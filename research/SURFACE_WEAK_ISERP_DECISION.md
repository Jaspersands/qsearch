# Surface Weak-IsERP: End the Local Attack Round

31 October 2026. Completed bounded classical-attack pass. The new Cayley
membership reduction is constructive; no classical kernel-recovery algorithm
was obtained. No native-hardness, novelty or speedup claim follows.

## What Changed

SURFACE_CAYLEY_MEMBERSHIP.md removes the polarized-source-map restriction
from the native descent test. For ell>=11, arbitrary a in End(E^2) is reduced
to a centered lift modulo ell, dilated to a polarized map on E^4, and tested
by interpolation on the OLD B^2 model. It pays an internal dimension32,
a global small-prime pool and the imported PPAV model. No new polarization,
large ell-torsion or target End/Hom lattice is required. An independent
review corrected one weak inequality and clarified canonical lift bounds.

Its Boolean-only query lower bound says membership cannot be renamed as
a polynomial-time saturation algorithm. Native geometric outputs remain
available to stronger attacks; the lower bound does not simulate them.
Do not create another membership backend or perturbation campaign.

## Published Lattice Algorithms Do Not Supply the Missing Lattice

Independent targeted reading of the retained Page--Robert--Soumier
[ePrint2026/276](https://eprint.iacr.org/2026/276), 48-page version, found:
Definition5.2 (p24) requires generators of the ENTIRE Hom group;
Theorem5.8 (pp25-26) computes with those generators, rather than finding
missing ones. Propositions5.16/5.19 (pp28-29) assume the required full
module/morphism correspondences. Remark5.22 (p30) starts from an explicit
smooth-degree path with accessible torsion. Theorem6.9 and Corollary6.11
(p33) start with Hermitian modules. None of these inspected statements
supplies target saturation from the present weak evaluator.

An arithmetic maximal overorder is not a geometric identification. In the
local symplectic space V=Z_ell^4 put R0=Z_ell I+ell M4(Z_ell). For every
Lagrangian W modulo ell let L_W be its inverse image in V. Then

    R0 subset End(L_W),       L_W^#=ell^-1 L_W.

The first inclusion follows from ell V subset L_W subset V; the dual
identity follows from W=W^perp. End(L_W) is a maximal order stable under
the same adjoint. Distinct W give distinct orders: a maximal matrix order
determines its lattice up to homothety, and these intermediate lattices
all have the same index. There are (ell+1)(ell^2+1) possibilities.
Thus rational algebra, R0 and adjoint data alone cannot choose the geometric
completion. This is a local nonuniqueness witness, not a hardness theorem
once native geometric data or integrality tests are present.

[Montessinos2601.18050](https://arxiv.org/html/2601.18050v1), Sections2.2–3,
also distinguishes a weak representation of the FULL endomorphism ring
from a weak representation of ONE isogeny. Those are different inputs.
The exact surface-conversion contract comparison remains the earlier
bundles/ppav-source-2026-10-23/PPAV_SOURCE_DECISION.md.

The full revised [Eisentrager--Scullard2402.05059v2](https://arxiv.org/html/2402.05059v2),
Theorem1.1/Sections6–7, still charges dependence on the largest bad prime
for general elliptic suborders. Its landing-page abstract omits that factor.
The existing bundles/local-order-scope-2026-10-26/SCOPE.md already records
this correction and the easier Bass cases. No general poly(log ell) surface
saturation theorem follows from this baseline.

## Inter-Query Isomorphisms: Exact Useful-Map Criterion

This characterization was derived and checked independently; it does not
supply an algorithm for choosing useful queries. Let
P_j=(B,lambda_B H_j), S_j=sigma_j^dagger sigma_j, and let
v:P_n->P_m be an actually computed polarized isomorphism. Define

    U=sigma_m phi^-1 v phi sigma_n^-1.

Then U^dagger U=I on the ORIGINAL source product, since
psi_j=phi sigma_j^-1 is ell-polarized onto P_j. The integral source pullback is

    beta_v=phi^dagger v phi=ell sigma_m^-1 U sigma_n.

Because both sigma's are integral units, beta_v is zero modulo ell if and
only if U is integral, in which case U is a polarized source automorphism.
Useful v's therefore correspond exactly to isomorphisms that do NOT lift
to such a source automorphism. This compares beta in the full known source
order, not an arbitrary target basis. Norm bounds follow from the known
sigma matrices and U^dagger U=I, so small-prime reconstruction is paid.

A marked same-kernel collision induces U=+/-I and gives zero. The identity
on the underlying B is generally NOT polarized between different H's.
On geometrically indecomposable +/-1 surfaces, stabilization does not create
a new useful map: cross-query pullback is C_m W F_n with v-block monomial W.
The source reductions of C_m,F_n are invertible modulo ell, so a nonzero
block pullback is present exactly when v is useful. A nonzero image gives
only partial K information; rank2 or the existing adjoint/word closure
certificate is still required for full recovery.

There is no established polynomial-time selection or useful-collision
probability guarantee. Merely searching geometric isomorphisms or retaining
all native intermediates is not such a guarantee. Do not build this search
without a new family or quantitative mechanism.

## Next Question Chosen by External Value

The next pass should decide the COMPLETE theorem and its contribution:

Does prime-only source -> known HPGP receiver -> certified K -> full algebraic
Hom/End output establish a weak-surface IsERP extension that removes a
substantive assumption or covers a native case absent from existing results?

This is one bounded theorem/priority audit, not another saturation variant.
The output step is NOT missing: bundles/kernel-output-2026-10-23/
KERNEL_TO_OUTPUT.md already constructs full algebraic module/order data from
correct K. The stronger effective-map route is in bundles/effective-output-
2026-10-23/EFFECTIVE_OUTPUT_AUDIT.md, with reference-curve, field, height and
model assumptions. Do not rediscover either as absent. That audit restricts
literal use of the geometric complexity theorem to ell<=p^C unless a separate
height analysis is supplied. Algebraic output and native evaluation differ.

Compare the precise promises against Chen et al.2305.19897 and the later
Chen--Petit full-suborder algorithm, using the retained prior-art and native
input audits FIRST. Distinguish removing a powersmooth-lifting assumption
from supplying the upstream native evaluator. No bare-target pathfinding or
cryptographic claim follows from a weak-evaluator theorem.

Independent selection review ranked this above fixed-q AG (no paid quantum
decoder/reduction) and renewed Rees application search (no new native source).
If the bounded audit finds only prior art, stronger-than-native input, or an
extension with no substantive assumption improvement/application, PARK this
line and compare independent mechanisms. Do not add dimension16/32 plumbing,
more local membership variations, or another source-parameter refinement.

Acceptance: one exact theorem with complete dependencies and a source-by-source
comparison, or a pinpointed failed obligation/known-result identification.
No generic novelty claim, outside contact, or submission is authorized.
