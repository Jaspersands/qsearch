# Target Endomorphism Coordinates Already Give A Classical Kernel Attack

2026-10-23. Constructive classical deduction and exact arithmetic controls;
independent proof/prior-art review pending. This is a stronger-input
baseline, NOT a break of the original weak-isogeny interface. No new quantum
algorithm, geometric implementation, or novelty certification is claimed.

## Decision

The source's representation-conversion gap cannot safely be filled by
supplying a full evaluable target endomorphism basis and its Rosati Gram
matrix. Those data, together with the existing weak torsion interface,
already recover the abstract large-prime kernel classically. A Hom(A,B)
basis and a compatible Hom module are NOT required for this attack.

The previous Hom-lattice attack remains correct. Its warning that End(B)
alone does not automatically provide Hom(A,B) is also correct, but does
not exclude this different attack. We reconstruct the integral maps

    F_a = phi a phi^dagger in End(B),

then test their divisibility by ell in the supplied FULL target lattice.
This reveals the entire algebra preserving K=ker(phi). Its trace-pairing
annihilator has image exactly K. No hidden ell-torsion points are built.

The original interface does not supply End(B), so it remains unresolved.
Further conditional receiver variants do not address that missing input.
No new native inverse-trace solver emerged from the separate triage in
this pass; no change to that branch's claims is justified.

## 1. Input Contract

Retain the source in SIEGEL_ELEMENTARY_REPOLARIZATION.md: principally
polarized A=E^g and B in characteristic p, ell an odd prime different from
p, and a polarized isogeny phi with

    phi^dagger phi = [ell]_A,   phi phi^dagger = [ell]_B.

K is Lagrangian in A[ell]. Require the following ADDITIONAL data and costs:

1. A full source End(A) basis a_i, exact evaluations, its Rosati form, and
   the public split End(A)/ell End(A) = M_(2g)(F_ell) in that same basis.
   These are available in the stated known-source-order model, not by
   evaluating at inaccessible ell-torsion points.
2. A full geometric End(B) basis b_j with exact evaluations, and the
   integral positive Gram matrix G_jk=Tr(b_j^dagger b_k). An abstract order
   isomorphic to End(B), without the specified evaluation correspondence,
   is NOT enough. Weak basis evaluations with unrelated unit scalars are
   also NOT enough. No Hom basis or Hom-module action is supplied.
3. Full accessible torsion bases on A[r] at sufficiently many DISTINCT
   small auxiliary primes r avoiding p*ell. The original weak evaluator
   gives Q=a_r phi(P), with one unknown unit a_r common to the full basis
   at each r. Exact point arithmetic and polarized pairings are charged.
4. Every field of definition, endomorphism description, evaluation cost,
   torsion construction, and small-prime discrete logarithm is paid.

Here D=rank End(A)=rank End(B)=4g^2. The geometric point-access argument is
for fixed g with polynomially bounded auxiliary primes. Uniform growing-g
torsion construction is not obtained for free. Separate auxiliary fields
are retained; no exponentially large CRT compositum is constructed.

Full lattices can be replaced by specified sublattices only after proving
containment of every F_a and the required saturation at BOTH the auxiliary
primes and ell. Successful small-prime evaluations do not prove the latter.

## 2. Scalar-Free Transport On Accessible Torsion

Choose compatible coordinates on A[r] and B[r]. Let W=a_r phi_r be the
matrix supplied by the weak images. It is invertible because r is coprime
to ell and a_r is a unit. Write A_i for the action matrix of the source
basis endomorphism a_i. The polarization identities give

    (F_(a_i))_r = ell * phi_r * A_i * phi_r^(-1)
                = ell * W * A_i * W^(-1).                 (1)

The unknown weak scalar cancels in the second line. The scalars at
different auxiliary primes need not agree, and none is recovered.

One can choose Q itself as the B[r] basis, in which case W is the identity
coordinate transport. Evaluate every b_j on Q and express those points
in Q using the nondegenerate original polarized pairing and paid small-r
discrete logarithms. Source actions are computed similarly in P.

Flatten the b_j action matrices into columns of T_r. These D columns are
independent: if a full-lattice endomorphism kills B[r], it factors through
[r], hence belongs to r End(B). Since D=(2g)^2, T_r is square invertible.
Solving the resulting linear systems gives EXACT coefficient residues
of every F_(a_i), not projective coefficient lines. No evaluator for
phi^dagger, arbitrary-point inverse of phi, or model for a new polarization
has been assumed.

## 3. Polynomial Integer Reconstruction

The Rosati norm of a transported basis map is known:

    ||F_a||^2 = Tr(phi a^dagger phi^dagger phi a phi^dagger)
              = ell^2 Tr(a^dagger a).                    (2)

The second equality uses cyclicity of trace and BOTH multiplier identities.
It is not a norm estimate for arbitrary unpolarized maps.

Write F_a=sum_j v_j b_j and S_a=ell^2 ||a||^2. In the positive form G,
Cauchy--Schwarz applied to the j-th coordinate functional gives

    |v_j|^2 <= S_a (G^(-1))_jj.

Let B_ja be the floor of the square root of this rational bound. Combine
the exact residues by ordinary integer CRT. If

    M=product(r) > 2 max_(j,a) B_ja,                      (3)

centered lifting gives the unique possible coefficient matrix. Check its
column norms against (2). Equality in (3) is insufficient: modulo2 the
bounded integers1 and-1 coincide. Insufficient M returns UNKNOWN, not a
hardness conclusion. No lattice reduction or sign enumeration is needed.

The bit lengths of G^(-1), S_a and M are polynomial in the supplied input.
Enough distinct polynomial-size small primes provide the required product;
their point/evaluation costs remain as above. A poorly conditioned basis
can increase the necessary M substantially and must use its ACTUAL Gram
matrix. A Euclidean coordinate bound in the wrong basis is invalid.

## 4. Divisibility Reveals The Hidden Stabilizer Algebra

Reduce the reconstructed D-by-D coefficient matrix modulo ell. It describes

    T: End(A)/ell End(A) -> End(B)/ell End(B),
       a |-> phi a phi^dagger.                            (4)

Its kernel is exactly P_K={a: a(K) subset K}.

Proof: phi^dagger(B[ell])=K. Inclusion follows from phi phi^dagger=[ell].
Both spaces have dimension g: phi^dagger is an ell-isogeny with g-dimensional
kernel inside the 2g-dimensional B[ell]. Thus F_a kills all B[ell] if and
only if phi a kills K, equivalently a preserves K. Since the target lattice
is full, killing B[ell] is equivalent to divisibility by ell in End(B).
Finally the source split map identifies its quotient with ALL matrices,
not just a supplied subalgebra of them. This proves (4).

In a basis with K the first g coordinates,

    P_K = { [A B; 0 D] },       dim P_K=3g^2.

Under the NONDEGENERATE pairing (X,Y) -> Tr(XY) on the full matrix algebra,

    P_K^perp = { [0 B; 0 0] },  dim P_K^perp=g^2.

The span of images of its matrices is precisely K. Trace pairing pairs
X_ij with Y_ji; replacing it with entrywise dot product reverses the
answer. Recover K by two nullspace computations and one image-span
computation. These are polynomial in g and log ell, including at large ell.

The implementation checks the expected dimensions, that all matrices in
the computed kernel preserve the recovered subspace, and that the result
is Lagrangian for the supplied alternating form. The preservation check
plus equal dimensions certifies equality to P_K as an abstract algebra.
These checks do NOT certify geometric provenance or identify a falsely
supplied lattice with the real End(B).

## 5. Attempts To Break The Argument

- **Only End(B), not Hom(A,B):** this is intentional. Formula (1) computes
  residues of endomorphisms, and (4) reads off a stabilizer algebra. No
  unconstructed Hom-module correspondence enters either step.
- **Independent weak masks:** a common unit at each level cancels. Different
  units on different basis points generally do not. Controls demonstrate
  the difference; the geometric input promise is still required.
- **Unknown adjoint evaluator:** only the identity phi^dagger=ell phi^-1
  on auxiliary torsion is used. Matrix inversion there is paid small-field
  arithmetic, not inversion on arbitrary geometric points.
- **An order is not the full endomorphism ring:** a local explicit suborder
  passes every tested auxiliary action-basis rank check, contains all F_a,
  yet gives the wrong divisibility kernel at ell. Fullness/saturation is
  a genuine precondition. Dimension checks reject this example, not every
  possible malicious input.
- **Wrong composition order:** swapping phi and phi^dagger can produce a
  perfectly valid but different Lagrangian. Algebraic self-consistency
  cannot correct an incorrectly identified source/target transport.
- **Correct rank alone:** countercontrols have the expected parabolic
  dimension but the wrong annihilator-image dimension, or both expected
  dimensions but no preservation. Both are rejected. A nonisotropic
  half-dimensional invariant space is rejected separately.
- **Abstract kernel versus geometric points:** output is K in the supplied
  source split representation. No large-prime point encodings or explicit
  isogeny factorization are output. This matches the proposed quantum
  receiver's kernel output, not an uncharged stronger task.
- **Original weak source:** it lacks the target ring/Gram data. This proof
  does not supply them, prove that a converter must reveal them, or give
  a classical algorithm for the original problem.

## 6. Prior Art And Research Consequence

Weak common-scalar evaluation and the need to pay point lengths are already
explicit in [Chen et al., Section2.4](https://arxiv.org/html/2305.19897).
Endomorphism-ring and isogeny/ideal connections are established background,
not a new discovery here. The factorization-through-multiplication and
Rosati trace facts use the same foundations as the earlier marking note;
see [Milne's Abelian Varieties](https://www.jmilne.org/math/CourseNotes/AV.pdf).
No exhaustive novelty search or independent theorem review is claimed.

The new project-specific consequence is a stricter source contract:
**neither a full Hom lattice NOR a full evaluable target End lattice with
Rosati Gram may be granted as harmless conversion advice.** Either enables
a classical attack on the intended abstract-kernel output. A bare abstract
order, a single endomorphism, a polarized model alone, and an efficiently
computable canonical label are NOT shown equivalent to this strong input.

The full PDF of [2026/1142](https://eprint.iacr.org/2026/1142) again returned
403 in this pass. Its abstract does not establish whether its conversion
algorithms accept the weaker interface. No bypass or theorem import was
attempted. Keep this as a precise literature dependency, not a project-wide
blocker. The next source result must construct conversion without either
strong lattice input, or show an access-matched classical attack. Do not
spend another pass adding conditional ring/marking variants.

## 7. Verification

`theorems/endomorphism_transport_recovery.py` implements scalar-cancelled
torsion-coordinate transport, exact Gram-bounded CRT reconstruction, and
the divisibility-kernel/trace-annihilator recovery. It has no CLI or registry
side effects. It does not construct geometric input data.

`tests/test_endomorphism_transport_recovery.py` has32 exact controls. The
global fixture uses actual identities in M_2(Z[i,j]), i^2=-1, j^2=-11, and
phi=diag(6+5i,6-5i). This suborder has index supported at2; the chosen odd
auxiliary primes and ell61 avoid that index, and every transported map is
in the fixture order. Its split matrices are finite algebra witnesses,
not executed curve arithmetic. Separate local controls include a 127-bit
secret prime, all2-by-2 matrices at primes3 and5, ill-conditioned bases,
independent scalars, bad norms and nonsaturation.

103 selected tests PASS in0.73s, including the prior Hom-lattice,
repolarization and marking suites; new-file Python syntax PASS. Live
arithmetic replay uses auxiliary primes(3,5,7,13), M=1365, and maximum
coordinate bound202. It recovers stabilizer dimension12, annihilator
dimension4, and kernel rows(1,50,0,0),(0,0,1,11) modulo61, matching the
independent reference. The receipt is
`research/classical_baselines/endomorphism_transport_recovery.json`.
No full-repository test run, coherent
quantum execution, natural-source dequantization or speedup claim follows.
