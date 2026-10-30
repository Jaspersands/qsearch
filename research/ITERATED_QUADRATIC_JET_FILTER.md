# Iterated Quadratic Maps: An Exact Classical Jet Filter

29 October 2026. A classical attack on the explicit iterated-map reserve,
not a new quantum algorithm, hardness result or claim of novelty. It
does not repeat the already implemented mixed-Frobenius lifting filter.
The question is whether exponential written degree conceals useful
nonabelian symmetry. Often a polynomial-time calculation of just the
linear and quadratic homogeneous terms proves that the symmetry is trivial.

## Problem And Decision

Supply a prime p>5, D=5m, a public quadratic polynomial map

    P_i(x) = c_i + A_i*x + x^T*B_i*x,       B_i symmetric,

a nonzero public linear observable ell, and a UNARY iteration count T.
Let Gamma=UT_5(F_p)^m act block-diagonally. The native problem is the
FORMAL stabilizer of F=ell composed with P^T under linear substitutions.
Forward and inverse substitutions give the same stabilizer. This is the
same public input, not an oracle promised to conceal a supplied subgroup.
The implementation also permits block sizes2 through5 for exact controls.

The existing fixed-fingerprint/Rees argument conditionally gives a quantum
route. It does not show classical hardness or a useful advantage. Circuit
evaluation has O(T*size(P)) cost and formal degree at most2^T; T and every
Frobenius, arithmetic and state-preparation operation remain charged.

Write the two-jet at the origin as

    F(x) = f_0 + b^T*x + x^T*B*x + terms of degree at least3.

Every linear symmetry of F fixes its homogeneous components separately.
Thus its exact finite stabilizer H is contained in

    K = {g in Gamma : b^T*g=b^T and g^T*B*g=B}.

K can be computed by linear algebra, with NO bound on the total degree
of F. If K is trivial, H is trivial. If K is nontrivial, this calculation
needs one of the completion certificates below; without one it must
remain UNKNOWN_FULL_STABILIZER.

## Exact Two-Jet Without Polynomial Expansion

After j iterations store

    P^j(x) = v + J*x + (x^T*C_i*x)_i + O(degree3).

Initially v=0, J=I, C_i=0. At the next step put

    U_i = A_i + 2*(B_i*v)^T,
    v'_i = c_i + A_i*v + v^T*B_i*v,
    J' = U*J,
    C'_i = sum_a U_ia*C_a + J^T*B_i*J.

Apply ell to the resulting vector coefficients. The matrices B_i and C_i
use the x^T*B*x convention: an off-diagonal entry contributes TWICE to
its corresponding monomial. No division by high factorials or differentiation
through formal p-th powers is used. Since p>5, the quadratic convention is
unambiguous. Nonzero constants are retained through the whole orbit v;
discarding them would give the wrong Jacobian and Hessian at later steps.

Dense implementation costs O(T*D^4) field operations and O(D^3) working
field entries. This is polynomial in the public input and numeric T,
which is why the unary iteration contract matters. The computation does
not expand2^T monomials, evaluate a full field table, assume an accessible
high-degree coefficient tensor, or test only base-field function equality.

## Exact Finite Quadratic Stabilizer

Let J_nil be the block-strictly-upper-triangular matrix algebra. Its
dimension is10m and J_nil^5=0, independently of total D. Compute the kernel

    L_K = {X in J_nil : X^T*B+B*X=0, b^T*X=0}.

These are O(D^2) linear equations in10m unknowns. Dense elimination has
O(D^4) field-operation cost. The following argument works even for a
singular B, without requiring p>D or p>4*degree(F).

For g in K, g^T*B=B*g^-1. For every k, `(g^T-I)^k*B=B*(g^-1-I)^k`.
The logarithm truncates after degree4, giving

    (log g)^T*B = B*log(g^-1) = -B*log g,
    b^T*log g = 0.

Conversely X^T*B=-B*X implies `(X^T)^i*B=(-1)^i*B*X^i`.
Truncated exponentiation therefore gives
`exp(X)^T*B*exp(X)=B` and `b^T*exp(X)=b^T`.
Terms of total matrix degree at least5 vanish, so this is valid already
at p=7; a degree-eight polynomial interpolation argument is unnecessary.

The kernel is a Lie subalgebra. With class at most4<p, exp/log identify it
with K, and exponentials of a basis generate K. This is the quadratic
baseline proved in CONSTRUCTIVE_ROUTE_FILTERS.md, now applied to a
COMPUTED component of an arbitrarily high-degree input, not just an
exposed scalar wrapper around a supplied quadratic.

The executable checks the kernel and returns its log basis. A zero kernel
is an exact certificate of the identity full stabilizer. It does not
silently turn a nonzero basis into generators of the full F stabilizer.

## Fixed Anchors And An Exact Completion Certificate

The origin is not the only legal expansion point. If a is fixed by every
g in Gamma, then `g*(a+u)=a+g*u`. The preceding proof therefore applies to
the two-jet of `F(a+u)` as well. For the block UT group, fixed anchors have
possibly nonzero FIRST coordinates in each block and zero other entries.
Initialize the recurrence with v=a, J=I, C_i=0. Intersect the linear
equations from all supplied, verified fixed anchors to obtain L_* and
K_*=exp(L_*). Always H is contained in K_*. Non-fixed anchors would not
justify this containment and are rejected.

A nontrivial upper group can sometimes be certified as the WHOLE answer
without expanding F. For each generator g=exp(X), X in a basis of L_*,
check the following exact public-coefficient identities:

    c = g*c,
    A*g = g*A,
    g^T*B_i*g = sum_j g_ij*B_j,  for every i,
    ell*g = ell.

The first three identities say `P(g*x)=g*P(x)` as FORMAL polynomials, not
only as functions on F_p. The fourth then gives `F(g*x)=F(x)` for every
nonnegative T. If all generators pass, they generate K_* inside H, and
the opposite containment from the jets proves H=K_*. These tests are
sufficient, not necessary: failure does not disprove a symmetry of F.
The implementation distinguishes upper-group generators from certified
full-stabilizer generators and leaves the latter unset on UNKNOWN.
For T=0 or1, the entire polynomial has degree at most2, so its two-jet
already proves equality even if the sufficient commutation test fails.
The report records this reason separately from actual propagation success.

With a anchors, dense jet generation costs O(a*T*D^4) field operations;
stacking their linear constraints and checking the returned generators
are polynomial in a and D. This does not assume a generic-point PIT
oracle or access to high-degree coefficients. A successful propagation
certificate solves the original stabilizer problem classically; it is
not evidence for a quantum advantage.

## A Large Family Of False Candidates

Take P(x)=x+Q(x), with Q homogeneous quadratic. Direct composition gives

    P^T(x) = x + T*Q(x) + O(degree3),
    F_2 = T*(ell*Q).

Suppose p does not divide T and the symmetric matrix B_0 of ell*Q has
all leading principal minors nonzero. Then K, hence H, is trivial.
Indeed such a form has a unique unit-upper-triangular congruence
factorization B_0=R^T*D_diag*R with nonzero diagonal D_diag. Conjugate an
upper-unitriangular isometry by R. An upper-unitriangular isometry of a
nondegenerate diagonal form is the identity, by successive columns.
The block group is a subgroup of this full unitriangular group.

For a uniformly random symmetric D-by-D matrix, this sufficient event
has EXACT probability `(1-1/p)^D`: there are
`p^(D*(D-1)/2)*(p-1)^D` such factorizations, out of
`p^(D*(D+1)/2)` symmetric matrices. If the coefficient matrices of Q
are independent uniform symmetric matrices and ell is any fixed nonzero
row, ell*Q is uniform. This is an ensemble statement for this specific
tangent-to-identity family, not all quadratic dynamical systems. Its
lower bound is at least1-D/p and need not be useful for fixed p and
unbounded D. The exact kernel test works beyond this sufficient event.

Thus increasing T until the old total-degree guard fails does not make
these instances difficult. In particular Q_0=sum_i x_i^2, ell=e_0 and
p not dividing T give a deterministic triviality certificate even when
the other coordinates of Q have mixed nonlinear couplings and2^T>>p.
These are falsifier controls, not proposed hard or useful quantum families.

## Characteristic-p Cancellation Is A Real Boundary

At T=p the tangent family loses this quadratic certificate. In fact ALL
degrees2 through p vanish. Let phi act on polynomials by pullback through
P=x+Q, and let N=phi-I. N raises positive homogeneous degree by at least1.
In characteristic p, the commuting-operator binomial identity gives

    phi^p = (I+N)^p = I+N^p.

The leading degree-raising part of N is the derivation
`delta_Q=sum_i Q_i*d/dx_i`. Hence, for linear ell, the degree-(p+1) term of
`ell composed with P^p - ell` equals `delta_Q^p(ell)`. The p-th iterate of
a derivation is again a derivation, as the intermediate Leibniz binomial
coefficients vanish in characteristic p. This is the familiar restricted
derivation operation, not a newly discovered algebraic primitive.

The first possible term can be zero, so it is not always the first
NONZERO term. For example P(x,y)=(x+y^2,y) satisfies P^p=identity exactly.
Do not promote cancellation or a failed jet certificate to hardness.

An explicit strictness control is p=7, Q=(y^2,x^2):

    delta_Q^7(x) = -x^6*y^2 + 2*x^3*y^5 - y^8.

Independent truncated formal composition agrees with this degree-eight
term. Embed x,y into the first two coordinates of the five-dimensional
map and leave the other coordinates unchanged. The two-jet of the scalar
observable is just x. The shear y->y+z lies in its jet stabilizer but
changes the displayed degree-eight polynomial. Consequently K is strictly
larger than H here. A nonzero jet kernel is genuinely inconclusive, not
a licence to return its generators as the original answer. The example
has easy unused-variable symmetries and establishes no hard instance.

In fact the ANCHORED test resolves this same control completely. The point
a=e_0=(1,0,0,0,0) is fixed by Gamma. Its first two coordinates follow

    (1,0) -> (1,1) -> (2,2) -> (6,6) -> (0,0),

and remain zero. The two-by-two Jacobian of P^7 at a is
`[[1,2],[3,4]]` over F_7. The gradients of F at0 and a are respectively
`(1,0,0,0,0)` and `(1,2,0,0,0)`. Their invariance forces the first two
rows of g to be those of the identity. The remaining lower UT_3 block
commutes with P and fixes ell. Therefore the full stabilizer is exactly

    H = diag(I_2, UT_3(F_7)).

The origin-only UNKNOWN record is retained as a soundness regression;
the two-anchor record solves the SAME public instance. This is a
classically resolved calibration, not a residual quantum application.

The one-dimensional version of delayed nonlinear terms in p-power
iterates is studied as lower ramification; see [Nordqvist's primary paper](https://arxiv.org/abs/1601.03622).
That literature is context, not an imported multivariate stabilizer algorithm.

## All Fixed Anchors Without Enumeration

30 October follow-up: James the 2nd proposed the following extension;
the parent checked the rank-increase argument and its field/access scope.
This is a written randomized classical procedure, not an implemented
extension-field backend or a claimed new general stabilizer theorem.

Let d=10m, V=Fix(Gamma), and Delta be a proved degree bound for F. Define
L_all as the F_p subspace of J_nil satisfying the linear/quadratic jet
equations for EVERY a in V over the algebraic closure. Coefficients of
these equations, viewed as polynomials in the anchor coordinates, have
degree at most Delta. Every actual symmetry lies in exp(L_all).

Choose a VERIFIED extension E=F_q with q>=2d*max(1,Delta)/epsilon. Take
d fresh independent uniform anchors in V_E, compute their two-jets,
and intersect the equations over F_p. In particular expand every E
coefficient in a fixed F_p basis; an E-linear kernel is not the answer.
The jet recurrence above works over E unchanged, while group matrices
and unknown Lie coefficients remain over F_p.

Conditional on the history, if the current F_p kernel is too large,
choose a direction outside L_all. Some violated scalar equation is a
nonzero polynomial of degree at most Delta in the anchor. A new anchor
misses that direction with probability at most Delta/q. Unless such a
miss occurs while the kernel is too large, its dimension falls by at
least one on every such probe. Starting in dimension d, d probes suffice.
A union bound gives failure at most d*Delta/q<=epsilon/2. This identifies
the kernel for ALL algebraic-closure anchors with the stated probability,
not merely for all base-field points. Every sampled kernel is an exact
upper constraint group regardless of whether sampling is complete.

Exponentiate a basis of the resulting kernel. At most d full-polynomial
identity tests, on F(g*x)-F(x) using FRESH independent extension points,
can check whether every generator actually preserves F. A union bound
spends at most the remaining epsilon/2. Passing gives a Monte Carlo
certificate H=K, not a deterministic identity certificate. Failing leaves
H properly contained in K, without finding its generators. A zero kernel
is already an exact triviality certificate and needs no probabilistic
completion claim.

For the unary iterated-map input, Delta<=2^T. Extension degree is
O(1+(T+log(d/epsilon))/log p), and the anchor calculations cost
O(d*T*D^4) extension operations plus polynomial F_p elimination. Full
identity tests use the original circuit, not expanded coefficients.
Verified irreducible-field construction, uniform field sampling and their
bit costs must be charged; any construction/sampler failure receives an
ADDITIONAL allowance or a corresponding split of epsilon. A seed is a
replay device, not evidence of independent uniform random choices.

Base-field anchors cannot replace extension anchors. For example at
p>5, F(u,v,z)=(u^p-u)^3*v has zero two-jet at EVERY (a,0,0), a in F_p.
At an extension a with a^p!=a its v derivative is (a^p-a)^3!=0, so the
fixed-origin shear v->v+z no longer preserves the jet. This example is
easy by the existing mixed-Frobenius filter; it only tests the access
distinction. The extension procedure is not currently exposed by the CLI.

## A Residual Orbit-Sum Family

Write the five-dimensional blocks as (u_i,w_i), with four transverse
coordinates per w_i. Supply homogeneous quadratic maps q and Q, allowing
couplings between blocks, and set

```
P(u,w) = (u+q(w), R(w)),       R(w)=w+Q(w),
ell(u,w)=sum_i u_i,            T=p in UNARY,       r(w)=sum_i q_i(w).
```

Then F_p=sum_i u_i+S(w), where

```
S = sum_(j=0..p-1) r composed with R^j = (phi-I)^(p-1) r,
phi(f)=f composed with R.
```

The identity follows from ((X^p-1)/(X-1))=(X-1)^(p-1) in F_p[X]. Since
phi-I raises positive homogeneous degree by at least one, S has no terms
below p+1. Thus EVERY fixed-anchor two-jet, including extension anchors,
is the linear observable plus its anchor constant. This is not an
inadequate anchor sample.

The linear component forces each block's first off-diagonal row to zero.
Consequently the exact remaining stabilizer is

```
H = diag(1, Stab_(UT_4(F_p)^m)(S)),
```

with the notation applied blockwise. Its ambient class is now three,
not four. The formal degree is at most 2^p and circuit evaluation costs
O(p*m^3) field operations for dense quadratic data. The coefficient input
has O(m^3*log p) bits, plus unary p. Because F_p has degree one in every
u_i, it cannot be a nontrivial-degree scalar postcomposition over F_p.
That fact does not eliminate other classical reductions of S.

A finite strictness control uses p=7, r=xy, Q=(y^2,x^2), with other
transverse coordinates unused. Its degree-eight term is
`-x*y^7+2*x^4*y^4-x^7*y`; the shear y->y+z changes it although every
fixed-anchor two-jet agrees. This low-dimensional control is easy, not
a proposed hard native family. Neither the general construction nor
this control has been shown to resist the orbit-module, structural,
Frobenius or higher-jet attacks, and no useful natural application is
established. The residual question is a general algorithm for these
public orbit-sum stabilizers, not a new accepted quantum candidate.

Carson the 2nd independently challenged the proposed application. S is
a ONE-HORIZON accumulated cost, not generally a dynamical first integral:
`S composed with R - S = r composed with R^p - r`. A symmetry of S need
not commute with R or define a quotient dynamical system. Recovering it
therefore does not automatically solve invariant discovery or model
reduction. A meaningful application must establish that missing link.

Before promotion, compare three additional classical structures:

- The actual recurrence symmetries `Q(Bw)=B*Q(w), r(Bw)=r(w)` give a
  subgroup of Stab(S). Their explicit quadratic representation has
  polynomial dimension, so the existing defining-characteristic Luks
  baseline applies. Containment must not be mistaken for equality.
- If `r=h composed with R-h`, then `U-h(w)` is a first integral of the
  skew product and `S=h composed with R^p-h`. Bounded-degree h can be
  searched for by linear coefficient equations. In particular r=ell*Q
  has the immediate solution h=ell*w; this can solve the invariant task
  without solving the terminal stabilizer task.
- If `R^j(w)=w+j*Q(w)`, the quadratic r makes r(R^j(w)) degree at most
  two in j. For p>3 its sum over j in F_p is zero. More generally a
  time polynomial of degree below p-1 gives the same collapse.

In the finite example, S_8=-x*y*(x^3-y^3)^2. The polynomial h=x^3-y^3
is killed by the vector field delta_Q, but
`h composed with R-h=-h*(3*x*y+x^3+y^3)` is nonzero. Infinitesimal
invariance does not supply an invariant of this discrete recurrence.
These checks leave the general residual question open; they do not
identify a hard family. No dynamical application is promoted by this pass.

## What This Enables And What It Does Not

This filter can solve a proposed instance classically or reduce the
remaining quantum question to the EXPLICIT subgroup K containing H.
The original fixed-fingerprint oracle restricted to K still hides H;
one need not generate or reuse a conditioned quantum source bank. Class
and derived rank of K must be recomputed before assigning Rees costs.
This written hybrid reduction is not a newly executed receiver.

Exact propagation is the implemented sufficient completion test above.
If a future implementation also tests all exp(basis) generators against the
full circuit by independent extension-field polynomial identity tests,
passing them can certify H=K with a charged error allowance. Such a test
is NOT part of the present backend. A generator failure only proves
H is proper in K; it does not give the missing generators of H.

The next substantive experiment would need a motivated p-power iteration
with nontrivial, unexposed symmetry that survives the full propagation
subgroup, sparse/orbit-module/Frobenius filters, and fixed-anchor jets.
Its first surviving restricted-derivation term is a concrete object to
attack. A truncated coefficient circuit for P^T(t*x) through degree p+1
has O(T*size(P)*p^2) gates using dense convolution, polynomial in the
unary input when T=p. That higher-jet backend is not implemented here.
More random T-not-divisible-by-p examples are low-value after
the exact argument above. Unresolved cases are not accepted candidates.

## Replay

    python qsearch.py iterated-stabilizer --write

For a new public instance:

    python qsearch.py iterated-stabilizer --input problem.json --write --output result.json

Supply an object with p, block_size, T, c, A, B and nonzero ell. T is
charged in unary. Coefficients must be canonical integers; B is a list of
D symmetric D-by-D matrices. For supplied fixed anchors, wrap the object
as `{"input": {...}, "anchors": [[...], ...]}`. The CLI fingerprints the
consumed bytes. An explicit output path is required when saving an input
run, so it does not replace the calibration artifact by accident.
Degree bounds and group cardinalities use exact `{"base": b, "exponent": e}`
expressions for b^e. Even a cheap high-T input can exceed Python's decimal
integer serialization limit if these powers are unnecessarily expanded.

This writes `research/classical_baselines/iterated_quadratic_jet.json` with
public input coefficients, exact jets, kernel and propagation records.
The deterministic high-degree calibration, a fixed-seed mixed map, the
origin-only p-iteration control and its two-anchor resolution are distinct.
Passing finite tests does not establish
the general proof; no quantum run, novelty or speedup status is promoted.
