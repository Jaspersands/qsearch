# A Regular Public Spectrum Leaves A Constant Kernel List

2026-10-25. Proposed local mathematical deduction and exact arithmetic
implementation. Independent review, formal verification and novelty
assessment remain pending. No geometric hiding function or incoming
surface isogeny was executed. This is a classical falsifier, not a new
quantum algorithm or a new oracle problem.

## Result And Decision

In the SAME weak surface-isogeny input used by the existing source, a
genuine publicly evaluable target endomorphism with squarefree degree-four
characteristic polynomial modulo ell suffices to produce at most SIX
candidate kernels. This does not require completing the target order.

The original source, IF implemented with its promised label equality,
selects the true candidate in at most 13 classical evaluations. With no
such evaluator, the result remains a bounded list, not a complete solver.
All costs of that evaluator remain charged. No replacement verification
oracle is granted. Unique-list cases do not need the evaluator.

This covers squarefree spectra that failed the previous stronger
all-Lagrangians-cyclic sufficient condition, including its unchanged ell=47
and ell=2^127-1 examples. The large-prime test is a local lattice control,
not a newly constructed native weak isogeny. Repeated spectra remain
outside this sufficient condition, not certified hard.

## Exact Input Contract

Retain phi:A=E^2 -> B with phi^dagger phi=phi phi^dagger=[ell], where ell
is an odd prime different from the characteristic. The principal
polarizations, full source order and its public abstract local splitting
are known. The geometric target order, a Hom basis, phi, its kernel K,
and geometric ell-torsion points are NOT supplied to the algorithm.

The old weak evaluator supplies W_r=u_r phi_r on full ordered auxiliary
bases, with ONE common unit per level and all levels from the same phi.
There must be sufficiently many usable fresh levels. Bounds, point
fields, basis construction, map evaluation and the common definition
field remain paid, exactly as in SOURCE_PULLBACK_ATTACK.md.

Require a genuine integral target map gamma, its paid auxiliary actions
and a norm bound. The old bounded trace-CRT reconstruction recovers exact
source-order coordinates of

    alpha = phi^dagger gamma phi,
    alpha_r = ell W_r^(-1) gamma_r W_r.

Also require the actual degree-four characteristic polynomial chi_gamma,
or its certified reduction modulo ell. For target model-field Frobenius,
the preceding completion module acquires it by auxiliary CRT with product
M>12q; no characteristic-polynomial oracle is added. The integral
controls here use a polarized multiplier-13 map, not characteristic-seven
Frobenius. The same Weil-type coefficient bounds apply to that map since
gamma^dagger gamma=13 and its complex eigenvalues have absolute value
sqrt(13). The implemented acquisition verifies this fixed control against
its exact reference polynomial.

For a general map, exact coefficients can instead be bounded using a
supplied Rosati norm and reconstructed by CRT. That generic acquisition
is NOT implemented here. It is not acceptable to attach an arbitrary
polynomial to unrelated local matrices. Arithmetic consistency checks
below are necessary, not certificates of genuine geometry.

### The Common-Field Frobenius Restriction

If E, B and phi are all defined over F_q and A is the product E^2 OVER
THAT FIELD, phi intertwines their q-Frobenius actions. On rational Tate
modules it is invertible, so

    chi_(B,F_q)(T) = chi_(E,F_q)(T)^2.

This polynomial is repeated over every residue field. Thus that common
field's Frobenius NEVER supplies the regular-spectrum premise here.
The useful Frobenius case needs an explicitly available smaller-field
target model for which phi or the product source is not defined over that
smaller field. Its coordinate-powering map remains available after base
extension. No unprovided descent, hidden isomorphism or free smaller-field
model may be assumed. The previous T^4+25 target control is not evidence
of an incoming E^2-isogeny over F_5. Arbitrary public non-Frobenius maps
are another possibility, but obtaining one is a real unresolved task.

## Existing Word And Lattice Tests

Adjoin alpha^dagger. The four products alpha_i alpha_j/ell are exact
source-order elements because they are pullbacks of target products.
The wrapper checks their integral coordinates before lifting the public
source splitting to ell^2. This chart is algebraic, not an ell-torsion
point oracle.

Let U be the span modulo ell of the first and second word images. They
are contained in K. On a surface, the preceding two-layer argument and
rank-one quotient construction give the following exhaustive branches:

* dim U=2: U=K, with no label queries.
* dim U=1: the first image is the same U. The divided actions induce
  explicit operators on the symplectic plane U-perp/U. Compatible kernels
  correspond exactly to their common invariant lines.
* dim U=0: alpha is divisible by ell in the full source order. Put
  beta=alpha/ell. The kernel is a beta-invariant Lagrangian plane.

The code uses the existing residual routine and independent prime-square
neighbor-integrality criterion. This pass does not replace their proofs
with a rank check or longer-word heuristic.

## Rank-One Spectral Divisor Lemma

The missing implication is that regular chi_gamma rules out a scalar
residual operator. Use the UNKNOWN genuine K only to prove this; the
algorithm never receives it. Choose an adapted symplectic Tate basis in
standard ordering (e1,e2,f1,f2) with U=<e1> and K=<e1,e2>. Neighbor
integrality writes the exact source action as

    alpha = [ ell A     B   ]
            [ ell^2 C  ell D ].

Since the images of alpha and its adjoint modulo ell are in U, modulo
ell the block B has only B11=b nonzero, where b!=0. The image of
alpha^2/ell is in U. Its (e2,f1) entry implies A21*b=0, so A21=0.
Its adjoint image is also in U, so alpha^2/ell kills U-perp. Its (e1,f2)
entry implies b*D12=0, so D12=0. All equalities in this paragraph are
modulo ell.

In the target neighbor basis the action of gamma is

    [ A B ]
    [ C D ].

Ordering that basis as (e2,e1,f1,f2) gives a block lower triangular
matrix with diagonal blocks A22, [[A11,b],[C11,D11]], D22. Consequently

    (T-A22)(T-D22) divides chi_gamma modulo ell.

On U-perp/U, in basis (e2,f2), the public divided action is

    beta_res = [ A22  B22/ell ] modulo ell.
               [  0     D22  ]

The upper-right entry uses two ell-adic digits. Its characteristic
polynomial is precisely that divisor. If chi_gamma is squarefree, then
A22 and D22 are distinct. Thus beta_res is non-scalar with two distinct
eigenlines. The other residual operators may remove lines but cannot
add any: at most TWO kernel candidates remain. Zero candidates would
contradict the genuine input promises. The implementation checks the
divisibility of this residual polynomial into the supplied chi.

This proof depends on adjoint closure and the second word layer. Neither
can be omitted. It does not extend to a scalar residual with repeated chi.

## Rank-Zero Enumeration Without Field Enumeration

Now beta=alpha/ell is integral and is conjugate to gamma over Q_ell,
since phi^dagger=ell phi^(-1). Its integral characteristic polynomial is
chi_gamma. Squarefreeness modulo ell decomposes the four-dimensional
source space into distinct simple F_ell[T]-modules.

Every invariant two-plane is a direct sum of a subset of these primary
components. If f is the product of its irreducible factors, then deg f=2
and that plane is ker f(beta). Conversely each such kernel has dimension
two and is invariant. There are at most four irreducible factors, at
most sixteen subsets to consider, and at most six subsets of total
degree two. Filter the resulting planes by the Lagrangian condition.

For a Lagrangian R invariant under beta, beta^dagger also preserves R:
for x,y in R, <beta^dagger x,y>=<x,beta y>=0. Thus these planes meet the
adjoint condition too. The independent prime-square neighbor test is
still executed. This identifies compatibility with the supplied algebra,
NOT geometric equality to the modeled B with all its weak markings.

## Selection Using Only The Original Source

The proposed original Sp4 source promises

    f(M)=f(N) iff M K=N K.

For nonzero v define the symplectic transvection T_v=I+v v^T J. It
preserves a Lagrangian K iff v lies in K. Indeed if v is not in K, some
w in K pairs nontrivially with v, and T_v w leaves K. If v lies in K,
the transvection fixes K pointwise.

For each candidate R, test its two basis vectors by comparing f(T_v)
with f(I). Both comparisons succeed iff R=K. With at most six candidates,
there are at most 1+2*6=13 evaluations of the SAME original source. The
code checks all listed candidates and rejects if there is not exactly
one match. This is not a proof of the source's global fiber promise:
a malicious finite callback may still mimic the tested labels.

The opaque labels in the tests check this interface only. They are not
an implementation, complexity measurement or replacement for the
unexecuted geometric source. The conditional implication is useful:
any valid efficient implementation of that original source can be used
classically to finish this subfamily, without its quantum HSP receiver.

## Costs And Falsifiers

After the existing bounded-CRT pullback, use fixed-dimensional products,
linear algebra, a degree-four finite-field factorization, and at most
one degree-two root computation in the rank-one branch. Factorization
is a standard randomized expected-polynomial-bit operation; no claimed
deterministic polynomial factorization is hidden here. The residual
square-root backend has a separate explicit cap and abort bound.
Its abort propagates, never becomes a zero-candidate report. All source
and field acquisition costs precede these bounds and remain charged.

The arithmetic controls are integral maps in M2(O_7), with
gamma=diag(3+2i,2+3i), gamma^dagger gamma=13. Their polynomial is
T^4-10T^3+50T^2-130T+169. They are easy product controls, not a hard
input distribution. Pullbacks are recovered from weak residue callbacks;
hidden phi is used only by fixtures and final truth checks.

| ell | phi diagonal | Word ranks | Candidate count | Original-label calls |
|---|---|---|---|---|
| 5 | 2+i, 2+i | 0,0 | 4 | 9 |
| 17 | 4+i, 3+i+j | 1,1 | 2 | 5 |
| 17 | 3+i+j, 3+i+j | 2,2 | 1 | 0 |

Every listed arithmetic plane also passes an independent quaternion
Hom-module integrality check. Complete small-field censuses compare
the whole returned set, not merely whether it contains the true kernel.
Other tests exercise second-layer rank growth, changed symplectic charts,
wrong spectra, inconsistent geometry, constant invalid labels and repeated
common-field Frobenius spectra. The old ell=47 and 127-bit T^4+25 local
controls each leave two candidates and use five label calls, without
changing primes. They do not construct a global isogeny with these lifts.

Most likely failure to matter: typical supplied targets expose only
scalar/repeated-spectrum maps, or no affordable valid geometric source
exists to select among the list. This result establishes neither a
general weak-isogeny solver nor classical hardness outside its premise.
No quantum signal survives because no quantum advantage was asserted.

Next work should obtain an actual geometric input/map or attack a
different constructive frontier. More local matrix grids, larger ell
alone, or renaming a repeated spectrum as difficult do not answer that.
