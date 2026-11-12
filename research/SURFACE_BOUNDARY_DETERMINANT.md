# Boundary determinants for the native surface comparator

2026-11-12. Parent derivation independently checked in
`audits/reviews/2026-11-12-boundary-determinant-repair.md`, fully parent-read.
This removes the parabolic-subspace/Kummer-transport obligation for the
CHARACTERISTIC POLYNOMIAL endpoint. Complete OPEN-module reconstruction is
still a separate upstream theorem. The completed paid boundary report was
also fully parent-read; its disposition appears below.
No quantum advantage, hardness, novelty or full comparator claim follows here.

Completed OpenAI target-boundary-determinant independently derived the same
boundary and final Leray formulas. Its warning about Pila1990's fixed-Q-family
scope is accepted. The actual Pila2005 all-field finite-stratification source,
checked by parent and independent reviewer, repairs that specific interface.
Its optional alternative using a supplied curve torsion primitive is UNNEEDED
and is not admitted as a native algorithm. Report agreement is not the proof.

## Exact conditional input and output

Let f:Y->P1/F_p be the cubic pencil blowup of a smooth quintic, with smooth
fibre genus31, 220 geometric singular fibres, each irreducible with one node.
Use odd ell!=p (ell>53 conservatively) and the actual untwisted sheaf
L'=R1 f_*Fell on U. Full Sp monodromy kills both its invariants and dual
invariants. Given the genuine arithmetic matrix Phi_W on

    W=Hom_GSp(Ndual,J_Cfull[ell])=H1(U,L')(2), dim W=13516,

one can classically recover the geometric parabolic characteristic polynomial
of degree96 in polynomial(log p,ell) bit time for this fixed native family.
For each CLOSED branch z, put f_z=deg z, q_z=p^f_z, let epsilon_z be +1 for
split node tangents and -1 otherwise, and let P_z be the zeta numerator of the
smooth genus30 normalization of that fibre over F_(q_z). Then

    B_W(T)=product_z (1-epsilon_z*T^f_z)*P_z(T^f_z),
    P_par(T)=det(1-T*Phi_W)/B_W(T) mod ell.                (A)

The degree of B_W is 220*61=13420. Division is exact polynomial division,
not eigenvalue matching. Shared factors and nonsemisimplicity cause no problem.
This identity does NOT reinstate the false ordinary-compact=parabolic theorem.
Ordinary compact-cover Hom remains OPEN cohomology.

## Proof, including both Tate twists

Leray for j:U->P1 and the skyscraper stalks of R1j_* give

    0 -> H1(P1,j_*L') -> H1(U,L') -> sum_z H1(I_z,L') -> 0.

The last obstruction H2(P1,j_*L') equals H2_c(U,L') and vanishes by dual
invariants. Use procyclic tame inertia, not the finite order-ell quotient.
For M the local nearby fibre, H1(I,M)=M_I(-1). The symplectic pairing
M x M -> Fell(-1) identifies M_I=(M^I)^dual(-1). Invariant cycles identify
M^I with H1 of the nodal fibre. Its normalization sequence gives eigenfactor
(1-epsilon*S)P_z(S), with no splitting assumption. Therefore local GEOMETRIC
boundary matrix is q_z² F_node^(-T), and its determinant is

    (1-epsilon_z*q_z²*T^f_z)*P_z(q_z*T^f_z).              (B)

The substitution T^f_z comes from Frobenius cycling the branch conjugates.
It is valid even when ell divides f_z. A split nodal elliptic fibre has
boundary Fell(-2), giving eigenvalue q² and checking the sign/twist exactly.

The actual W output is arithmetic on the twist(2); its boundary matrix is
F_node^T, giving B_W in (A). The remaining quotient is arithmetic on P_par(2).
Parabolic duality identifies P_par(2)=P_par^dual: use perfect Poincare pairing
H1_c x H1 -> Fell(-2), the self-adjoint map H1_c->H1 and its nondegenerate
symmetric induced form on the image. Hence arithmetic on P_par(2) has the
same characteristic polynomial as GEOMETRIC on P_par. This proves (A),
without silently exchanging arithmetic and geometric Frobenius on OPEN H1.
Alternatively use geometric open matrix p² Phi_W^-1 and boundary (B).

## Native classical boundary computation and source scope

Each closed branch degree is<=220. Its unique geometric node is rational over
that residue field. Blow up that point in P3 and take the strict transform;
this resolves the ordinary node, including the nonsplit case. Graph embedding
in P3 x P2 and Segre give a smooth curve in P11 of degree28 and genus30:
(2H-E).Ctilde=2*15-2. Fixed-variable saturation/elimination has fixed degree
and polynomial log(q_z) bit cost. Tangent discriminant's quadratic character
computes epsilon_z without splitting its roots.

Actual Pila2005, arXiv:math/0504570, TheoremsD/E/F (and alternative H) provide
finite all-field stratification into COMPLETE Jacobian atlases and uniform
polylog(q_z) zeta computation for these fixed curve presentations. E removes
the rational divisor input. The 1990 fixed-Q curve theorem ALONE would not
pay native uniformity. Root and independent reviewer read the actual 2005
proofs in audits/sources/legendre_prf/pila_curve_families_0504570.txt.
Finite precomputation depends only on the fixed family, not the varying input.
Branch and base-locus factoring have fixed degree and bounded randomized
polylogp cost, with exact output checks. No growing-genus point-count oracle.

## Full degree53 determinant and CRT

All fibres are connected and irreducible, so R0f_*Fell=Fell,
R1f_*Fell=j_*L', R2f_*Fell=Fell(-1). Vanishing H0/H2 of R1 kills the relevant
Leray differentials. H2(Y) has graded pieces Fell(-1),P_par,Fell(-1), hence

    P2_X(T) = (1-pT)^2 P_par(T)
        / product_(b CLOSED in base scheme)(1-p^deg(b)*T^deg(b)).

The base scheme has degree45; the result has degree96+2-45=53. This uses
filtration determinants and the blowup formula; no rational section or
section-sum projector is required. Multiply back to check exact divisions.
Smooth hypersurface integral cohomology is torsion-free in the relevant
range, so these determinants are reductions of the integer Weil polynomial.
CRT modulus>2^54 p^53 suffices by coefficient bounds. The needed primes
ell>53,ell!=p have largest size O(logp); all numerical-ell work is polynomial
logp at fixed n,r. For any required fixed-polynomial threshold p<=Q(ell),
direct counts over extension degrees<=53 cost p^O(1)<=Q(ell)^O(1), paying
that fallback explicitly. Finally #X(Fp)=1+p²-[T]P2_X.

All formulas above remain conditional on the GENUINE complete open Frobenius
input. They neither construct that input nor replace its reconstruction
height/field obligations. The earlier supplied-module Kummer filter remains
valid in scope, but is no longer required for this endpoint.
