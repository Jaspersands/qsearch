# The Complete Rank-One Target-Algebra Test

2026-10-24. Local deduction and exact arithmetic implementation. Independent
review and novelty assessment pending. No geometric source or quantum
algorithm was executed. This is a classical falsifier for a specified
subfamily of the existing surface source, not a new oracle problem.

## Decision

The old source-pullback word test can stop at a certified kernel LINE even
after all words have been exhausted. The existing Frobenius residual note
uses a second ell-adic digit, but assumes one skew map squaring to -p.
That special identity is unnecessary for a useful general refinement.

For ANY supplied target maps and their adjoints whose word-image span
stabilizes at a line U, their already recovered source pullbacks induce
an explicit algebra on U-perp/U. Its common invariant lines are EXACTLY
the kernels compatible with integrality of the supplied target algebra.

- One non-scalar residual operator leaves at most two candidates. Other
  operators can remove candidates, including leaving a unique answer.
- If every residual operator is scalar, all ell+1 extensions are compatible.
  No longer word or additional ell-adic precision can improve this PARTICULAR
  integrality test using the same algebra. This is not a hardness result.
- A unique candidate needs no geometric label evaluation. Two candidates
  are separated by the existing two-call test on the SAME proposed Sp4
  source; both calls retain their full geometric implementation cost.

This gives a stronger classical admission gate, not a Shor-level result.
The largest application gap is still acquiring useful target maps from
actual public geometry on targets not already covered by earlier attacks.

## Input And Existing Reconstruction

Retain phi:A=E^2 -> B, phi^dagger phi=phi phi^dagger=ell, ell odd and
different from the characteristic. K=ker(phi) and L=ker(phi^dagger) are
Lagrangian. The full source order, its actions and positive trace Gram
are known; no target order, Hom basis, secret phi, or ell-torsion points
are given to the extraction algorithm.

Require actual additional integral target maps gamma_1,...,gamma_s, their
paid small-torsion actions, and norm bounds. The prior source-pullback
method reconstructs EXACT source coefficients

    alpha_i = phi^dagger gamma_i phi,
    (alpha_i)_r = ell W_r^(-1) (gamma_i)_r W_r,

using weak full-basis images W_r=u_r phi_r and bounded CRT. All original
weak-input consistency, norm, field and point-access promises remain.
There are no additional weak queries in the new refinement.

Adjoin adjoints. Products satisfy alpha_i alpha_j = ell alpha_(gamma_i gamma_j).
Their division is justified by this identity, not by an unrestricted
saturation oracle. Lift the PUBLIC source algebra splitting to ell squared
using the existing idempotent lift. This is not geometric ell-torsion access.

Let Gamma denote the resulting adjoint-closed set. Run the old word test
first. Rank two already recovers K; rank zero remains a separate problem.
The present input is precisely the stabilized rank-one case:

    U = sum_i im(alpha_i mod ell), dim U=1,
    im(alpha_i alpha_j / ell mod ell) subset U for every i,j.

The old two-layer completeness proof shows why no longer word increases
U on genuine surface inputs. The implementation verifies the pairwise
conditions rather than assuming stabilization from a status string.

## Quotient Construction And Proof

Write Lambda=T_ell(A), V=Lambda/ell Lambda and W=U-perp. Since the alphabet
is adjoint-closed, EVERY alpha_i mod ell kills W. Thus W has dimension
three, contains U, and W/U is a nondegenerate symplectic plane.
For v in W define

    beta_i([v]) = [alpha_i v_tilde / ell mod ell] in W/U.

Four checks are needed; omitting any can create a false quotient map.

1. Divisibility: alpha_i kills W modulo ell, so division makes sense.
2. Lift independence: v_tilde -> v_tilde+ell z changes the value by
   alpha_i z mod ell, which belongs to U.
3. Quotient independence: express u in U as a sum of alpha_j z_j modulo
   ell. Its divided image is a sum of alpha_i alpha_j z_j/ell modulo ell,
   plus terms in U, and is therefore in U by the pairwise condition.
4. Image in W: the adjoint of alpha_j alpha_i/ell is another reversed
   pair product. Its image is in U, so that pair product kills W modulo
   ell. It follows that alpha_j(alpha_i v_tilde/ell)=0 modulo ell for
   every j. The common kernel is W because the adjoint image span is U.

These arguments use the exact source order and only TWO ell-adic digits;
no Frobenius square, skewness or semisimplicity assumption is present.
The induced adjoints agree with the quotient symplectic adjoints.

## Exact Compatibility, Not Just A Necessary Test

For any Lagrangian plane K' containing U, K' is inside W. The neighboring
lattice is Lambda_(K')=Lambda+K'_tilde/ell. Integrality of the rational map
alpha_i/ell on this lattice is equivalent to

    alpha_i Lambda subset ell Lambda+K'_tilde,
    alpha_i K'_tilde subset ell^2 Lambda+ell K'_tilde.

The first condition follows from im(alpha_i mod ell) subset U subset K'.
The second is exactly beta_i(K'/U) subset K'/U. Conversely any Lagrangian
compatible with every supplied map contains U by the first condition,
and therefore arises this way. Thus the correspondence is a bijection
between compatible K' and common invariant lines of the beta_i.

Preservation of a lattice by all generators implies preservation by every
integral sum and product of them. Hence this classification already includes
the ENTIRE generated target algebra, not only words up to a cutoff. Away
from ell, the original prime-to-characteristic ell-isogeny changes no Tate
lattice. Compatibility with the algebra does NOT certify that the resulting
quotient is the supplied modeled B with its original weak markings.

If all beta_i are scalar, every projective line is invariant. If some beta
is non-scalar, compute its degree-two characteristic polynomial. An
irreducible polynomial gives no line, a repeated root gives one Jordan
eigenline, and two distinct roots give two lines. Filter these against ALL
other operators. The scalar case must not be confused with the repeated-root
non-scalar case. Zero candidates contradict the genuine input promises;
they are not evidence for classical hardness.

For two distinct resulting planes K0,K1, choose v in K0 outside K1. The
public transvection I+v v^T J fixes a Lagrangian precisely when it contains
v. Comparing its ORIGINAL hiding-function label with the identity label
selects the true plane in two calls, as in the earlier Frobenius note.
Finite opaque labels test this interface only; they are not a geometric
oracle implementation or a new search benchmark.

## Costs And Scope

After prior bounded-CRT reconstruction, use O(s^2) fixed-dimensional
source products/divisibility checks, a polynomial-bit public chart lift,
fixed-dimensional field linear algebra and at most one square root in
F_ell. The reused root backend has an explicit trial cap and abort bound
2^(-cap) under independent uniform draws. Aborts propagate, not empty lists.
The degree-two root routine does not factor ell-1 or enumerate the field.
Exact source coefficients and norm bounds have polynomial-size bit lengths;
the fixed word depth does not silently expand them exponentially.

The scalar output retains ell+1 symbolically, not as an enumerated list.
All new postprocessing is randomized polynomial bit time with explicit
failure accounting; the old reconstruction and any final label costs remain.
No expected quantum advantage is claimed. Instead, a quantum claim on this
subfamily must beat this stronger classical test on the SAME actual input.

## Decisive Controls And Self-Attack

The integral controls use the known maximal order in (-1,-7), ell=11,
phi=diag(2+ij, b), and gamma=diag(j, c). Both diagonal factors of phi
have norm eleven. These are product-target ARITHMETIC controls, already
easy by other methods, not naturally difficult geometric instances.

| b | c | Old word-image ranks | Compatible kernels |
|---|---|---|---|
| 2+j | 1+j | 1,1 | 2 |
| 2i+j | 2i+j | 1,1 | 1 |
| 2+j | 1 | 1,1 | 12 |

The first two target maps have minimal polynomial degree FOUR over Q,
so these are not scalar shifts of the old quadratic Frobenius case.
Recovery uses only weak residue callbacks, bounds and the known source
order. Hidden phi is confined to fixture callbacks and final comparison.
Every completion of the returned line is checked against the independent
quaternion Hom-module integrality criterion, not just the new eigenline test.

Other falsifiers include all 81 two-by-two operators over F3 against all
40 Lagrangians, complete selected F5 fibers, incompatible common lines,
noncommuting residual maps, changed prime-square charts, symplectic basis
changes, exhausted root budgets and a 127-bit local arithmetic control.
The same FIRST digit admits 0/1/2/ell+1 outcomes when the second changes.
Higher-digit changes cannot affect this local integrality condition.

The reason this may fail to matter broadly is explicit: a generic
indecomposable B need not provide a useful known gamma, let alone a
non-scalar residual algebra. Rank zero or a scalar residual does not supply
a solver. Conversely the familiar absence of a full mixing map is no
longer a sufficient reason to retain a rank-one instance as unresolved.

This is a local composition of standard lattice and invariant-subspace
ideas with the existing access-matched reconstruction, not a claimed new
general theorem in arithmetic geometry. The weak-isogeny setting and
quantum elliptic result are prior work:
[Chen et al., IsERP](https://arxiv.org/abs/2305.19897).
The previous SOURCE_PULLBACK_ATTACK.md and FROBENIUS_RESIDUAL.md remain
valid within their scopes; this note refines their rank-one boundary.

Next useful work must supply actual geometric maps/input, attack the
remaining scalar/rank-zero cases by DIFFERENT information, or validate
the full geometric source. More matrix sizes or longer words in the same
algebra do not answer that question.
