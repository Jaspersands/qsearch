# Elementary Action Lifts And The Remaining Polarization-Model Gap

2026-10-23. Constructive deduction, independent proof/prior-art review pending.
This is not a completed isogeny HSP oracle or a new cryptanalytic algorithm.
The tests are exact quaternion identities, not geometric or quantum execution.

## Decision

For A=E^g, g>=2, with efficiently known supersingular End(E), every queried
Sp_(2g)(F_ell) matrix has an efficiently evaluable degree-ONE automorphism
lift of the underlying abelian variety. Composing the given isogeny with
the inverse lift moves its kernel as required. No powersmooth isogeny lift
is needed for this particular operation.

The lift generally does NOT preserve the product polarization. We can
derive the correct transported principal polarization, prove it integral,
and compute its action on accessible auxiliary torsion without knowing
End(B), the secret ell-torsion, or the weak evaluator's unit scalars.

This removes an action-evaluation obstacle in a narrow, explicit input
model. It does NOT supply an efficient geometric model for the transported
polarization or its jointly marked canonical label. Raw evaluator strings
fail the HSP promise; abstract torsion and pairing labels also fail it.
The next task is the representation-conversion theorem in Section 6,
not additional nearby quaternion examples or rigidity bounds.

The [2026-10-30 conversion audit](WEAK_SIEGEL_CONVERSION_AUDIT.md) checks
the accessible primary literature and a concrete stabilization route.
Its source-side Gram completion is constructive, but the natural
complementary map has pullback NI-ell H^-1, not H. In dimension two,
direct scalar repair forces ell|N. Independently signed weak torsion
images also do not directly meet exact graph-interpolation inputs.
The full2026/1142 text remains inaccessible; the original gap stays open.

Follow-on classical baseline: SIEGEL_HOM_LATTICE_BASELINE.md proves that
supplying a full evaluable Hom(A,B) lattice and its Rosati Gram matrix
allows projective modular reconstruction of phi. Compatible right module
action then recovers its abstract kernel classically. Such strong input
must not be silently added to repair conversion. This does not dequantize
the original interface here, which does not provide that lattice.

SIEGEL_ENDOMORPHISM_TRANSPORT_ATTACK.md now rules out a second repair:
supplying a full evaluable End(B) basis and its Rosati Gram matrix. Weak
torsion images then reconstruct a -> phi a phi^dagger; divisibility modulo
ell reveals the kernel's stabilizer algebra and hence the abstract kernel
classically. This does NOT need a Hom(A,B) module. A converter must avoid
both strong lattice inputs; a bare abstract ring is not shown sufficient.

## 1. Input And Actual Output Task

Fix odd characteristic p and an odd prime ell!=p. Let E be supersingular,
O=End(E), and A=E^g with its product principal polarization, g>=2. Require:

- A basis, structure constants, dual involution and efficient point
  evaluators for O, all over explicitly represented fields.
- An efficient original polarized model (B,lambda_B) and a weak evaluator
  for an ell-isogeny phi:(A,lambda_A)->(B,lambda_B). Thus phi^dagger phi=ell
  and geometric degree(phi)=ell^g. Weak evaluation on each auxiliary order
  r has ONE unknown unit scalar common to the full basis, not per point.
- Accessible full bases on separately represented auxiliary A[r], with
  pairwise coprime orders avoiding p*ell, as in the marking note. Their
  construction, fields and point lengths remain costs, not free advice.

The intended output of the quantum reduction is the hidden Lagrangian
K=ker(phi) as an ABSTRACT F_ell-subspace in a specified split presentation
O/ell O=M_2(F_ell), extended to M_g(O). It is not an explicit list of kernel
points over a potentially exponential extension. Computing End(B) from
that abstract K requires an additional module/representation conversion;
do not silently declare that second task solved either.

One obtains a split presentation from the known algebra, not by first
evaluating on inaccessible E[ell]. The dual involution becomes the usual
symplectic adjoint, so matrices for the acting group are public. This is
the algebraic rather than geometric torsion-coordinate approach familiar
from [Chen et al., Section 4.1](https://arxiv.org/html/2305.19897). Their
elliptic group-action construction is prior art; the present product
argument changes the computational question, not their theorem.

## 2. Constructive Degree-One Lifts

Use interleaved coordinates (e1,f1,e2,f2,...), with symplectic form
J=diag(J2,...,J2). A physical elementary matrix e_ij(c)=I+cE_ij can be lifted
as follows. If i and j are in different elliptic factors a,b, choose q in O
whose 2-by-2 reduction has its single nonzero entry c at those positions.
The quaternionic elementary matrix

    I_g + E_ab(q)

is an actual automorphism of E^g, with inverse I_g-E_ab(q). Its reduction
is e_ij(c). A lift of q is computed by solving a four-dimensional linear
system modulo ell in the known O basis. No norm equation is involved.

If i,j belong to the SAME elliptic factor, choose k in another factor.
Then

    e_ij(c) = [e_ik(c),e_kj(1)]
            = e_ik(c)e_kj(1)e_ik(-c)e_kj(-1),

and all four factors now have cross-factor lifts. This is why g>=2 matters.
It is not a construction of large automorphism groups on an elliptic curve.

Every M in Sp_(2g)(F_ell) lies in SL_(2g)(F_ell). Gaussian elimination gives
a polynomial-length elementary word for M. Signed row exchanges are
elementary products, and determinant-one diagonal corrections follow from

    w(a)=e_12(a)e_21(-a^(-1))e_12(a),
    diag(a,a^(-1))=w(a)w(-1).

Distribute the final diagonal into such two-coordinate corrections. Lift
each elementary factor as above, retaining the inverse word. The result is
sigma_M in Aut(A) with sigma_M mod ell=M, plus an explicit inverse.
Neither the individual factors nor sigma_M need preserve lambda_A.

All word lengths are polynomial in g and log ell. Intermediate quaternion
coefficient bit lengths are bounded by the word length times the input
basis/multiplication-table bit lengths plus log ell and log g. Evaluate
elementary maps using the supplied O evaluators and point addition. Do not
expand their potentially high-degree rational maps. This supplies a
uniform arithmetic construction, not an assumed strong-approximation or
powersmooth-lifting oracle.

## 3. The Correct Polarization Formula

Set sigma=sigma_M and

    psi_M = phi sigma^(-1),            ker(psi_M)=M K,
    S_M = sigma^dagger sigma = I + ell T_M.

The last divisibility is in M_g(O), because M is symplectic and the known
split presentation respects adjoints. Define

    H_M = I + phi T_M phi^dagger
        = (1/ell) phi S_M phi^dagger
        = phi S_M phi^(-1),
    lambda_M = lambda_B H_M.

H_M is integral by the FIRST formula; do not implement rational division
on points as if a canonical division operation were free. It is symmetric
for lambda_B. Moreover

    psi_M^dagger H_M psi_M = [ell]_A.

Since M K is Lagrangian for the original lambda_A, the polarized quotient
theorem gives a unique principal polarization on the codomain B of psi_M
whose pullback is ell lambda_A. Its rational endomorphism is precisely
H_M by the displayed identity. This proves that lambda_M is genuinely
principal and positive; no unjustified assertion that every symmetric
endomorphism is a polarization is needed.

One can also certify that H_M is an integral automorphism. Since
S_M^(-1)=sigma^(-1)sigma^(-dagger)=I+ell T'_M,

    H_M^(-1) = I + phi T'_M phi^dagger.

For norms, conjugacy gives Tr(H_M^2)=Tr(S_M^2). Thus a bound on the
lambda_B-Rosati squared norm of H_M is computable from public sigma and O,
with polynomial bit length. This is a bound for a proposed conversion
algorithm, not evidence that such a conversion exists.

The construction keeps the SAME underlying B and changes its principal
polarization. It is therefore consistent with the previous counterexample
to ignoring polarizations. It does not evade that counterexample by
pretending sigma was polarized.

## 4. What Can Actually Be Evaluated From Weak Data

psi_M(P) is weakly evaluated as phi(sigma^(-1)(P)), with the original unit
scalar at order r. Since sigma is an automorphism it preserves point order.

There is a useful scalar cancellation for the polarization on accessible
auxiliary torsion. Let P be an ordered basis of A[r], and write its weak
images as Q=a_r phi(P). This is a basis of B[r] because a_r and ell are units
modulo r. If W_r denotes this basis transport, then

    H_M|B[r] = W_r (S_M|A[r]) W_r^(-1).

The unknown scalar cancels. One does not need an evaluator for phi^dagger
or the value of a_r to compute this action. For small prime auxiliary
orders, coordinates in Q can be obtained using the original polarized
Weil pairing and small-order discrete logarithms; the nondegenerate pairing
matrix is inverted over F_r. Using brute force for these discrete logs
costs polynomial in r, NOT log r. This is acceptable only when those
auxiliary primes are polynomially bounded in the actual input length.

Point availability is still separate. At fixed g the crude Frobenius-order
bound for a prime r is polynomial in r; it is not polynomial uniformly in
g. Do not create a large CRT compositum, grant a large-prime torsion basis,
or turn this finite-torsion evaluator into an arbitrary-point inverse for
phi. The construction has not produced a theta model for (B,lambda_M).

The marking level sufficient to distinguish ell-isogeny kernels is not
automatically sufficient to distinguish all larger-norm H_M. A conversion
using additional torsion to identify H_M must select and pay for it using
the H_M norm bound. Its evaluations still have the stated torsion-only
interface, not a supplied arbitrary-point adjoint or good representation.

## 5. Two Attempts To Get Labels Still Fail

### Raw Transported Data Are Not Constant On Cosets

Take g=2, ell=61, E:y^2=x^3-x in characteristic 11, and its automorphism
i with i^2=-1. Write s=6+5i, t=6-5i and phi=diag(s,t). The actual degree
is61^2 and the multiplier is61. Use

    sigma = [[1,61],[0,1]],   sigma mod61=I.

Then ker(phi sigma^(-1))=ker(phi), but H_M is NOT I and the auxiliary
markings in the unchanged coordinates on B generally differ. Nevertheless

    u = (1/61) phi sigma^(-1) phi^dagger

is an integral automorphism, u phi=psi_M, and u^dagger H_M u=I. The marked
polarized objects are equivalent. Labeling by the raw polarization program
or the raw tuple of point coordinates would split one genuine HSP coset.

This example uses two lifts of the identity to expose lift dependence;
a deterministic lift choice alone is not a proof of equality for different
matrices in the same hidden-stabilizer coset. That promise still needs the
correct geometric canonicalization.

### Abstract Torsion/Pairing Canonicalization Erases The Secret

For any M,N and every r coprime to ell, the rational map

    u_NM = psi_N psi_M^(-1)
         = (1/ell) phi sigma_N^(-1) sigma_M phi^dagger

acts invertibly on B[r]. There it carries the exact M-markings to the
N-markings and is an isometry from lambda_M to lambda_N. These relations
hold EVEN WHEN M K != N K. At the geometric level u_NM is an actual
automorphism exactly when the kernels agree. If the kernels differ, its
ell-adic denominator cannot disappear; it is not a morphism of varieties.

Thus arbitrary isomorphisms of the abstract auxiliary torsion modules
preserving the transported pairings do not suffice. All these local
data are compatible with a rational map whose integrality fails at ell.
One must constrain the label equivalence to actual geometric isomorphisms,
as required by SIEGEL_MARKED_SOURCE_RIGIDITY.md.

The focused test uses a nontrivial symplectic elementary word and checks
different61-kernels, a nonzero numerator modulo61, and valid marking/pairing
isometries at every tested auxiliary prime. These are exact countercontrols,
not a hardness proof for every canonicalizer using richer geometric data.

## 6. The Remaining Constructive Question And Updated Prior Art

The needed primitive is now precise:

    Input: an efficient polarized model (B,lambda_B), a succinct positive
    symmetric integral automorphism H defining lambda_B H, a public norm
    bound, and the accessible evaluation data actually supplied above.
    Output: an efficient polarized model for (B,lambda_B H), with point
    transport sufficient to canonicalize the WHOLE marked object.
    Cost: polynomial in log p, log ell and the charged representation
    lengths for fixed g; no secret ell-torsion, End(B), or module basis.

Do not substitute a named general-purpose canonicalizer for this input
conversion. Do not assume that a public H evaluator reveals the full
endomorphism lattice of B. Once an appropriate polarized model exists,
the marking theorem and one shared codomain isomorphism supply the desired
equality promise. Coherent compilation, field encodings, bounded failure
and workspace cleanup would then still need checking.

The source audit found relevant 2026 work that was missing from this branch:

- [Corte-Real Santos--Piasecki--Wesolowski, 2026/1142](https://eprint.iacr.org/2026/1142)
  announces a theta-model computational
  framework, automorphism algorithms, higher-dimensional interpolation,
  and canonical compact representations. The
  [author's April slides](https://jc2-2026.sciencesconf.org/file/1366992)
  explicitly formulate operations on ALREADY encoded PPAVs. The full paper
  PDF returned403 in this session. Do not assert from its abstract or those
  earlier slides that it either solves or excludes the change-of-polarization
  input conversion above. Inspect its full definitions and conversion
  lemmas before importing a theorem. Canonical isogeny representation and
  geometric kernel recovery are also different output tasks.
- [Page--Robert--Soumier, 2026/276](https://eprint.iacr.org/2026/276)
  provides conversion tools with an ABSTRACT MODULE REPRESENTATION as input.
  Such a representation for the unknown target is not supplied here. Its
  existence cannot be substituted for an efficient way to recover it.
- [Montessinos, Theorem3.5](https://arxiv.org/html/2601.18050)
  distinguishes good from effective endomorphism representations and
  relates explicit isomorphisms and IKO matrices under stated assumptions.
  Its full equivalences for products must not be imported unchanged for
  Jacobians. In particular, an efficient abstract endomorphism action is
  not automatically the required target lattice, polarization coordinates
  and differential data.

The first paper is an important prior-art lead, not a newly proved
dependency. Its later full statement could close this gap, or establish
that the apparent new construction is already standard. Either outcome
is more valuable than further finite examples.

## 7. Failure Review And Next Decision

What was constructively reduced: Sp matrix -> actual unpolarized unit word
-> transformed isogeny evaluator -> integral principal polarization formula
and exact accessible-torsion action. None requires the secret kernel.

What remains unproved: efficient model conversion and canonicalization
under this weak input, the final useful target-output conversion, and a
classical analysis for the resulting GEOMETRIC labels. The earlier opaque
random-label lower bound does not establish natural-input hardness.
If full accessible ell-torsion becomes an assumption, compare against
ordinary abelian HSP before claiming any new quantum benefit.

Decisive next work: audit2026/1142 for this exact repolarization input
contract, then attempt the conversion or an access-matched classical
reconstruction. Stop this source branch if the only available conversions
assume the target module/ring or the hidden kernel. Do not create additional
conditional lift variants to avoid that decision. Independent constructive
directions remain available; there is no overall project/user blocker.

## Validation Scope

tests/test_siegel_repolarization.py has22 passing focused checks. It uses
the order Z[i,j], i^2=-1, j^2=-11, with odd test primes avoiding11. Actual
endomorphism identities in this order support the controls, while its
split2-by-2 matrices expose the torsion-coordinate algebra independently.
The same-factor commutator, inverse words, Rosati congruences, corrected
polarizations, scalar cancellation and both label failures are tested.

Final combined selected milestone:179 tests PASS in1.99s. Python syntax
checks pass for the new test and the preceding marking module/test;
targeted whitespace checks pass. This is not a full-repository test run.

No curve arithmetic, torsion generation, model conversion, canonicalizer,
quantum receiver or asymptotic timing claim was implemented. Helpers stay
inside the focused test module deliberately; they are not a new backend
or an admitted candidate. No central registry, CLI/UI or Git writes.
