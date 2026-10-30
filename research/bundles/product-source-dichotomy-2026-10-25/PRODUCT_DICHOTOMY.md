# Product Targets: A Complete Source-Side Dichotomy

2026-10-25. Local written deduction, independently unreviewed. This composes
the existing source-pullback attack with the product polarization. It is not
a new quantum algorithm, a novelty claim, or a geometric implementation.

## Decision

An explicitly product-polarized target is not a genuinely new surface
search family under the current weak-isogeny contract. For a prime-to-p,
ell-polarized map E^2 -> E1 x E2, with full known source order:

1. A factor-projector pullback nonzero modulo ell reveals the entire kernel
   by classical linear algebra and bounded small-torsion CRT.
2. Otherwise the isogeny is monomial in the GIVEN product factors. It splits
   into two degree-ell elliptic weak-isogeny instances, with no extra oracle,
   point halving, full target order or Hom-module advice.

The earlier product-corner gate left its nontransverse branch UNKNOWN.
This closes that branch as a REDUCTION, not as a classical solution. The
elliptic problems can remain unresolved under restricted query access.
The first branch also avoids reconstructing the full target lattice.

## Input And Access

Retain one actual phi:A=E^g -> B=product_i E_i with PRODUCT principal
polarizations and phi^dagger phi=phi phi^dagger=[ell]. Here g is fixed,
p>3, and ell is an odd prime distinct from p. Source End(A)=M_g(End(E))
is given in full integral coordinates, with its Rosati pairing and a
faithful public split modulo ell. The target product projections e_i are
ACTUAL available maps, not a decomposition inferred from superspeciality.

At each allowed small auxiliary prime r, W_r=u_r phi_r acts on the entire
ordered source basis with ONE common nonzero scalar. All levels refer to
the SAME phi. Small-torsion point access, fields and compatible frames are
paid as in source-pullback-2026-10-23. A sufficiently large CRT modulus is
required. A short fixed transcript is not silently extended.

The proof below works for fixed g. The new executable classifier is ONLY
for g=2, reusing the previously checked quaternion-order and CRT code.

## 1. Reconstruct The Source Projectors

Define alpha_i=phi^dagger e_i phi. These are actual integral source maps.
Their auxiliary actions are

    alpha_i mod r = ell W_r^(-1) (e_i mod r) W_r.

The unknown scalar cancels. These maps satisfy exact identities

    alpha_i^dagger=alpha_i,
    alpha_i alpha_j = delta_ij ell alpha_i,
    sum_i alpha_i = ell I,
    Trd(alpha_i)=2ell,
    ||alpha_i||_Rosati^2=2ell^2.

Consequently each pairing with a known source basis vector a has magnitude
at most floor(sqrt(2ell^2 ||a||^2)). The existing bounded CRT reconstruction
with target-map squared norm 2 recovers each alpha_i in the full known
source order. Integral Gram inversion does not require a target order.
The bit cost is polynomial in the paid norm/field/input sizes, NOT in ell.
The implementation rejects an insufficient level plan before observations.

## 2. Why Each Row Is Either Active Or Isolated

Work in symplectic Tate coordinates modulo ell. Put

    M=phi mod ell, K=ker(M)=im(M^dagger),
    L=im(M)=ker(M^dagger), B[ell]=orthogonal_sum_i V_i.

K and L are Lagrangian of dimension g. Let P_i project onto the symplectic
plane V_i, and set r_i=dim(P_i L). Orthogonality gives

    L intersect V_i = (P_i L)^perp inside V_i,
    dim(L intersect V_i)=2-r_i.

Here L=L^perp. Since L intersect V_i is also a subspace of P_i L,
2-r_i <= r_i, and r_i cannot be zero. Hence r_i is 1 or 2.

If r_i=1, P_i L=L intersect V_i is a line. Thus M^dagger P_i M=0.
If r_i=2, P_i M is surjective onto V_i, and M^dagger is injective on V_i
because L intersect V_i=0. Thus alpha_i mod ell has rank TWO and

    im(alpha_i mod ell)=M^dagger V_i.

This proves the rank dichotomy without extrapolating from finite tests.

In the rank-zero case, faithfulness of the source split implies
alpha_i in ell End(A). Then beta_i=alpha_i/ell is an INTEGRAL self-adjoint
idempotent of reduced trace 2. No general saturation oracle is used.

Every such beta_i in the product-polarized M_g(End(E)) is one of the
STANDARD factor projectors e_j. To see this, its diagonal entries are
Rosati-fixed quaternions, hence rational algebraic integers, hence integers.
The identity beta_i^2=beta_i expresses each diagonal entry as a sum of
nonnegative integral norms of its row entries. Their sum is one because
Trd(beta_i)=2. Exactly one diagonal entry is one; all other rows vanish,
and self-adjointness eliminates the corresponding columns. The remaining
row therefore has no off-diagonal entry either.

Since phi alpha_i=ell e_i phi, cancellation in the torsion-free Hom group
gives

    e_i phi = phi e_j.

This isolates target factor i and source factor j. Its sole map
psi_i:E -> E_i has psi_i^dagger psi_i=ell, hence degree ell. Distinct
rank-zero target projectors isolate distinct source factors: the beta_i
are pairwise orthogonal. The result uses the PRODUCT source polarization;
it is false to replace it with an arbitrary principal polarization.

## 3. Recover Everything Except Explicit Elliptic Lines

Delete the isolated source/target pairs. The remaining map phi_active is
still ell-polarized between the remaining products. Every remaining row
has r_i=2. Therefore

    span_i im(alpha_i mod ell)
        = sum_i M_active^dagger V_i
        = ker(phi_active mod ell).

If s pairs were isolated, this known subspace has dimension g-s, and

    K = K_active direct_sum_j ker(psi_j).

There can be no exactly one-dimensional active component: its only row
would necessarily have r_i=1 and would already have been isolated.

For g=2 this leaves precisely two branches. Both projectors are nonzero
modulo ell and either one's rank-two image is K; or both vanish and phi is
monomial. A single zero projector and a rank-two partner is inconsistent
with the genuine input. The implementation checks the complementary exact
identities, not only a rank computed from untrusted residues.

## 4. Reduction Preserves The Original Weak Interface

For each isolated pair (target i, source j), a legal query on a source
point or complete basis embedded in factor j, followed by target projection
i, gives u_d psi_i(P). The same unit masks a full elliptic basis at level d.
No division, doubled torsion level or extension beyond the original point
field is needed. A batch-only surface interface is handled by filling out
the other source factor basis and retaining the appropriate output block.

The two elliptic masks inherit correlations from the original source;
solving the two instances separately is a valid reduction, not a claim
that these correlations contain no further classical information. A solver
for the exact restricted elliptic problem suffices to recover the original
abstract kernel in its PUBLIC source chart. The reduction neither executes
that solver nor grants the arbitrary-point interface used by stronger
published elliptic algorithms.

For comparison, the established elliptic weak-isogeny formulation is in
[Chen et al., Definition 2 and Sections 4-5](https://arxiv.org/html/2305.19897v1).
Its arithmetic and access assumptions must be audited separately; see the
existing bielliptic-source note. This pass does not remove them.

## Falsifiers And Boundaries

- Wrong or deficient source order: the divisibility and standard-projector
  conclusions need not follow. Existing CRT checks require its discriminant.
- Arbitrary modeled Jacobian: there are no supplied product projections.
  Geometric superspeciality does not make them computable for free.
- Non-product source polarization: integral projections need not be the
  standard coordinate projections. The monomial conclusion is not licensed.
- Inconsistent maps across levels or basis-dependent masks: finite checks
  do not authenticate the global weak-isogeny promise.
- Insufficient torsion transcript: no exact pullback reconstruction follows.
- Rank-zero output is NOT a recovered kernel, dequantization certificate,
  elliptic speedup, or evidence of classical hardness.

The exact arithmetic controls use constructed quaternion maps only to
generate masked observations and independently check answers. The extractor
receives no hidden phi, K, full target order or target Hom module. These
controls do NOT instantiate geometric surfaces or prove the imported CRT
access model feasible for an arbitrary input. No full native quantum
workflow was run. The general modeled Jacobian source remains unresolved.

Adversarial checks include insufficient legal levels, nonfaithful public
source splitting, malformed projector identities, mismatched factor
routing and an INTEGRAL unpolarized shear. The last produces genuine
idempotents that are not Rosati-self-adjoint; the classifier rejects them.
The fixture computes its public mod-ell algebra chart by small enumeration.
That is not a polylogarithmic implementation and does not query hidden
ell-torsion points. The extractor takes the promised public chart as input.
