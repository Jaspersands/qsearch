# Exact Boundary of Automorphism Harvesting on the Surface Source

31 October 2026. Deduction checked independently by a second Codex agent.
This bounds a specified classical extractor. It does not establish hardness,
a query-distribution estimate, or a quantum advantage.

## Statement

Use the prime-only source in SURFACE_SOURCE_RECONCILIATION.md, with ONE
fixed genuine ell-polarized phi:A=E^2->B. For any set of group queries j,
let S_j=sigma_j^dagger sigma_j and H_j=phi S_j phi^-1. Suppose EACH queried
P_j=(B,lambda_B H_j) is geometrically indecomposable and has only the
origin-preserving polarized automorphisms +1 and -1. This is an explicit
promise, not an assertion that random queries satisfy it frequently.

For each actual source quotient q_j:B^8->Y_j, allow the classical competitor
the COMPLETE unmarked Aut(Y_j), including its geometric evaluations.
Harvest every B->B corner of q_j^dagger v q_j. The dagger here is the
polarized adjoint from Y_j to the ORIGINAL B^8. Close these corners under
addition, composition, original-polarization adjoint and integer scaling,
using arbitrarily many qualifying queries. Also allow division by an integer
coprime to ell whenever the resulting map is independently known integral.

Every resulting map gamma satisfies

    phi^dagger gamma phi = 0 mod ell End(A).

Thus every image used by SOURCE_PULLBACK_ATTACK.md's word-image extractor
is zero. Extra word length or noncommuting queries does not repair this
particular extractor. The known exact division by ell when multiplying two
pullbacks is included and does not violate this conclusion.

## Proof and Correct Adjoint

The construction supplies C_j,F_j in M8(Z[H_j]), with

    F_j=H_(j,8)^-1 C_j^dagger,
    F_j^dagger H_(j,8)=C_j,
    u_j q_j=F_j,

where u_j:Y_j->P_j^8 is polarized. The inverse H_j^-1=t_j I-H_j is integral,
so every entry of F_j is an integral polynomial. We need u_j only in the
proof; the classical competitor need not compute it.

Unique decomposition into polarized indecomposable factors implies
Aut(P_j^8)={+1,-1}^8 semidirect S8. This uses [Ibukiyama, Karemaker and Yu,
Theorem4.20](https://arxiv.org/html/2205.13180v3#S4.SS5), whose full statement
and proof were checked in the primary text. The automorphism permutes the
embedded factors and restricts on each to a polarized automorphism of P_j.
The prior bundle POLARIZATION_COMPLETION.md already used the decomposition
statement for projectors; the present deduction covers the complete
unmarked automorphism group under the additional +/-1 promise.

For v in Aut(Y_j), put W=u_j v u_j^-1, a signed permutation matrix. Then

    q_j^dagger v q_j
      = F_j^dagger H_(j,8) W F_j
      = C_j W F_j.

Omitting H_(j,8) would use the wrong polarization. Every corner is therefore
some integral polynomial P(H_j). Since phi^dagger=ell phi^-1,

    phi^dagger P(H_j) phi = ell P(S_j).

This is divisible by ell in the known FULL source order. For mixed queries,
conjugation by phi^-1 sends each generator P(H_j) to P(S_j), integral in
End(A). It preserves sums and products. Because phi is polarized, conjugation
also preserves the adjoints for the original polarizations; H_j itself is
self-adjoint. Hence the same conclusion holds for every generated word,
even if H_i and H_j do not commute.

For a certified integral delta with n delta=gamma and gcd(n,ell)=1,
let beta_delta=phi^dagger delta phi in End(A). Then
n beta_delta=phi^dagger gamma phi=0 modulo ell. Invertibility of n proves
the same zero residue for beta_delta, and closure persists thereafter.
For actual target words gamma eta, the standard attack computes

    beta_(gamma eta)=beta_gamma beta_eta/ell.

Both initial factors have an ell, so the actual word pullback retains one.
This operation differs from assuming gamma/ell is integral on the target.

Moreover the UNORDERED collection of reconstructed source-coordinate
pullbacks of a full list at one qualifying query is predictable from public
source arithmetic:

    { ell [C_j(S_j) W F_j(S_j)]_ab : W a signed permutation, 1<=a,b<=8 }.

There are 2^8*8! such W, a fixed but large constant. This does not simulate
how the native routine names automorphisms, geometric encodings, marked
correspondences or the entire source output. No classical simulation of
the quantum experiment follows.

## Strongest Countercontrols and Exact Scope

An independent target map need not satisfy the conclusion. On the product
control with phi=[[6,5],[-5,6]], ell=61, the map diag(1,-1) pulls back to
[[11,60],[60,-11]], whose action on abstract E^2[61] has rank2 and recovers
K. That is the existing easy classical fixture, not a generic source.

A separate Sage control used the two source shears
sigma_1=[[1,61],[0,1]], sigma_2=[[1,0],[61,1]]. Their integral H_1,H_2 do
not commute. The pullbacks of H_1,H_2,H_1H_2,H_2H_1,H_1H_2H_1 all have
rank0 on the four-dimensional torsion space, and
beta_1 beta_2/61=beta_(H_1H_2) exactly. This tests arithmetic orientation
and mixed words; this product fixture does NOT satisfy or verify the
indecomposable-geometric promise above. The all-query statement is the
proof, not an extrapolation from this control.

Parent replay: tests/test_siegel_reverse_transport.py, 56 passed with
warnings as errors, plugin autoload/bytecode/cache disabled. No native
automorphism group, PPAV quotient or hidden kernel was generated in this
new pass. Existing informative target maps remain allowed classical inputs
only when actually computable from the original geometry.

Uncovered operations include ell-primary saturation/integral division,
new geometric isomorphisms between DIFFERENT queried polarizations,
canonical geometric invariants and marks, independent target maps, and
queries with decomposable or extra-automorphism P_j. Existing integer
coordinates may be useful to other algorithms. No assertion is made about
the density of qualifying queries or the cost of finding exceptional ones.

## Decision and Next Test

Do not build more word harvesters for this branch. The scientifically useful
next classical attempt must derive ell-primary integral information or a
new inter-query map from the SAME weak input, with a paid recovery proof.
Those operations cannot be supplied as a target End/Hom lattice. Failure
of such an attempt leaves the problem UNKNOWN, not hard. The recovered
conditional source remains worth assessing as a complete algorithm and
against prior art; this extractor boundary alone is not positive evidence.
