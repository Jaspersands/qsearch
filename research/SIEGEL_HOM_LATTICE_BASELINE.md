# A Supplied Homomorphism Lattice Gives A Classical Attack

2026-10-23. Constructive classical baseline and exact arithmetic controls.
Independent review pending. This is an application of lattice reduction,
not a claim of a new lattice algorithm or a break of the original weak
isogeny input. No geometric lattice construction is implemented.

Follow-on: SIEGEL_ENDOMORPHISM_TRANSPORT_ATTACK.md gives a DIFFERENT attack
using a full evaluable End(B) basis, its Rosati Gram matrix and the weak
torsion data, without constructing Hom(A,B). The statements below about
End(B) not automatically supplying a Hom module remain true; they must
not be read as security of the stronger target-ring input.

## Decision

The proposed Siegel source must NOT repair its polarization-model gap by
quietly supplying a complete Hom(A,B) lattice with evaluable basis maps
and its Rosati Gram matrix. With those data, sufficiently many accessible
weak torsion marks reconstruct the isogeny's primitive coefficient vector
classically, despite an independent unknown unit at EVERY auxiliary prime.
With the compatible right End(A)-module action, its abstract large-prime
kernel is then recovered by linear algebra, without constructing points
on the secret large-prime torsion.

This strengthens the existing warning about target module advice. It does
not establish that every target endomorphism description or every PPAV
conversion algorithm supplies these data. In particular, it does NOT show
that the original input of SIEGEL_ELEMENTARY_REPOLARIZATION.md is easy.
That input lacks the Hom lattice. A geometric conversion that avoids it
remains a live possibility, not a theorem disproved by this baseline.

## 1. Exact Additional Input

Let A,B be principally polarized g-folds in characteristic p, and let
phi:A->B have multiplier ell, an odd prime different from p. Its geometric
degree is ell^g and its squared Rosati norm is S=2*g*ell. Besides the weak
torsion interface in the existing source note, the attack requires:

1. A Z-basis b_1,...,b_D of Hom(A,B), with exact evaluators on the accessible
   auxiliary torsion. Alternatively, a specified full-rank sublattice
   containing phi suffices if reduction is injective at all chosen primes
   and primitivity is established in that lattice.
2. The positive definite INTEGRAL Gram matrix
   G_ij=Tr(b_i^dagger b_j), in that same basis, and a valid squared norm
   bound S. The trace/integrality convention is the one in the marking note.
3. At distinct small primes r coprime to p*ell, full ordered torsion bases
   with actual point coordinates and computable pairings, plus weak images
   a_r*phi(P_j), where a_r is one unknown NONZERO scalar for the entire basis.
4. For abstract kernel recovery, compatible right End(A)-module action
   matrices in this Hom basis and a public split presentation
   End(A)/ell End(A) = M_(2g)(F_ell). These are not secret-torsion points.

The first two items are NOT consequences of having an efficient model of B.
They must be supplied or constructed with their cost charged. In the
superspecial product setting D=4*g^2 for the full Hom lattice. Fixed g is
still necessary for the previously stated auxiliary point-field budget.

For each r, flatten the torsion action of every b_i into a column of T_r.
Its columns are independent over F_r: a homomorphism that kills all A[r]
factors through [r], and so belongs to r Hom(A,B). This is where fullness
of the lattice, or the stated good-reduction substitute, is used.

Express the weak point images in a B[r] basis using pairings and charged
small-order discrete logarithms. Solving T_r c_r = weak_images gives

    c_r = a_r * v (mod r),       phi = sum_i v_i b_i.

Thus one obtains a nonzero PROJECTIVE coordinate vector c_r, without
learning a_r. All field/basis transport must use the same public models.
The implementation starts at these coefficient vectors; it does not
pretend to construct geometric torsion coordinates.

## 2. An Exact Integer Reconstruction Certificate

Put M=product(r) and form the full-rank integer lattice

    Lambda = {z in Z^D : z mod r belongs to span(c_r) for every r}.

Each prime contributes D-1 independent linear congruences; therefore
[Z^D:Lambda]=M^(D-1). A row basis is constructed by successively imposing
one congruence on an integer basis. For a nonzero row-functional value
at pivot j, multiply row j by r and subtract its appropriate multiples
from the other rows. This is polynomial integer arithmetic, not enumeration
of the r possible scalars or of candidate isogenies.

For v,w in Lambda, all coordinates of v wedge w are divisible by M. If
v,w are independent, the induced positive Gram form on the exterior square
is integral, and hence

    ||v wedge w||^2 >= M^2,
    ||v wedge w||^2 = ||v||^2 ||w||^2 - <v,w>^2
                   <= ||v||^2 ||w||^2.

Consequently, for ANY nonzero compatible primitive vector w of squared
norm W<=S, the STRICT inequality

    M^2 > S*W

certifies that every compatible vector of squared norm <=S is rationally
collinear with w. Primitive integral vectors on this line are exactly
w and -w. The certificate proves uniqueness in this supplied lattice,
not the original input's geometric promises or the norm bound's truth.

This is a certificate even if the procedure finding w is imperfect. The
code separately checks every nonzero projective mark AFTER primitive
normalization: dividing a lattice vector by its coordinate gcd can lose
a congruence when that gcd is divisible by an auxiliary prime.

Strictness is essential. At M=2 with Euclidean Gram matrix, (1,1) and
(1,-1) have the same projective mark and squared norm 2; M^2=S*W=4.
No uniqueness conclusion follows at equality or below the threshold.

## 3. Polynomial-Time Sufficient Budget

Apply classical LLL to Lambda with its supplied Gram form. The classical
short-vector bound gives a nonzero output w with

    ||w||^2 <= 2^(D-1) * lambda_1(Lambda)^2
             <= 2^(D-1) * S.

Thus the sufficient input-independent budget

    M^2 > 2^(D-1) * S^2

forces w to be collinear with the promised phi vector. Primitive
normalization recovers v up to sign, provided phi is primitive.
For an ell-polarized isogeny it is: if phi=[k]psi with |k|>1, then
k^(2g) divides deg(phi)=ell^g, which is impossible. The global sign does
not affect the kernel.

The logarithmic torsion budget is O(D+log S). Polynomially many small
primes can supply it, without a large CRT compositum. LLL and the exact
positive-Gram arithmetic have polynomial bit cost in the supplied basis,
Gram matrix and congruence sizes. Auxiliary point construction/evaluation
is additional paid work; this calculation does not prove its availability.

LLL is prior art: [Lenstra--Lenstra--Lovasz, 1982](https://ir.cwi.nl/pub/9304).
The implementation uses [FLINT's Gram representation](https://flintlib.org/doc/fmpz_lll.html)
and verifies the integer basis transformation and reduced Gram matrix.
Exact rational Gram-Schmidt checks use delta=9/10, eta=3/5; since
delta-eta^2>1/2, the displayed squared-length bound follows. The requested
FLINT parameters (0.99,0.51) are stronger than these validation thresholds.
The final uniqueness decision uses the measured W, not an unverified
floating-point estimate or the nominal LLL guarantee.

## 4. From Coefficients To The Abstract Kernel

Let R=End(A), with the supplied split R/ell R=M_(2g)(F_ell), and suppose
the compatible right R-module action on Hom(A,B) is available. After
recovering v, compute the kernel of the F_ell-linear map

    R/ell R -> Hom(A,B)/ell Hom(A,B),      alpha |-> phi alpha.

Under the isogeny and lattice promises this is the right ideal

    J = {alpha : image(alpha|A[ell]) is contained in K},
    K = ker(phi|A[ell]).

Indeed phi alpha is divisible by ell in Hom exactly when it vanishes on
A[ell]. In the split matrix algebra J consists of ALL matrices whose
columns lie in K. The span of columns of a linear basis of J is therefore
exactly K. This is an abstract F_ell computation, not evaluation on a basis
of geometric ell-torsion. It uses phi alpha, NOT alpha phi.

The module action can also be constructed if a genuine full evaluable Hom
basis, the Gram data and source End(A) maps/norms are supplied. Evaluate
b_j alpha on auxiliary torsion, solve for its coefficients modulo small
primes, and reconstruct integer coefficients with a certified bound. If
T bounds its squared norm, each coefficient obeys

    |coordinate_i|^2 <= (G^(-1))_ii * T.

For example ||b_j alpha||^2 <= ||b_j||^2 ||alpha||^2 supplies such a bound
using positive Rosati forms. Use enough exact CRT data for the coordinate
bounds, with all fields and evaluations charged. This is a specification,
not an implemented geometric module-construction routine.

## 5. Falsifiers And Research Consequences

- Missing Hom basis/Gram or unknown target module: this attack is NOT an
  algorithm for that input. Do not report the original source dequantized.
- A basis only for End(B) does not by itself supply a compatible Hom(A,B)
  module or identify the original phi by THIS attack. The follow-on
  transport attack nevertheless recovers the abstract kernel from a full
  evaluable End(B) basis, Gram and weak torsion data. Check the actual input.
- Wrong/nonfull lattice, false norm bound, inaccessible torsion or
  noninvertible/per-point masking invalidate the stated input contract.
- Small M is UNKNOWN, not hardness. The primitive-normalization and
  equality-threshold controls prevent two false positive certificates.
- Separate auxiliary signs are not a global sign. Pairing-derived square
  roots at separate primes do not remove their independent CRT choices.
  The integral norm bound plus the supplied Hom lattice is the extra
  ingredient in THIS recovery, not a free pairing argument.
- Compact reconstruction of phi alone is not a large-prime kernel basis.
  Section 4 explicitly supplies and pays the additional compatible module
  action used for abstract kernel recovery.

The useful next geometric question is still conversion WITHOUT these
strong inputs. Rechecking all three authors' publication pages found only
links to ePrint2026/1142, not an accessible full theorem. Its applicability
to the weak-polarization interface remains unverified. Do not use the
abstract or a module-input theorem to claim this step closed.

## 6. Artifacts And Verification Scope

- `theorems/projective_lattice_reconstruction.py`: congruence lattice,
  exact positive-Gram/LLL checks, and a strict exterior-product certificate.
- `tests/test_projective_lattice_reconstruction.py`: independent scalars,
  large coordinates, ill-conditioned bases, index identities, boundary
  ambiguity, lost marks, incorrect norm bounds, and the right-ideal kernel
  formula. The quaternion-coordinate fixture has 16 lattice coordinates.

These are exact arithmetic controls, not curves, isogeny evaluation,
quantum execution, a complete geometric attack or a formal Lean proof.
The existing Lean project IS present; its Rees draft and required cache
files remain partly offloaded. No compiler run was attempted through those
files, and no hydration, cache repair or relocation was performed.

Validation:23 new tests and71 selected tests PASS in0.47s; new-file Python
syntax PASS. The direct16-coordinate quaternion run used primes
(3,5,7,13,17,19), M=440895 and squared norm244, and recovered the expected
primitive coefficients. This does not certify the original geometric
input model, all repository tests, or an independently reviewed theorem.
