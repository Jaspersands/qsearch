# Prime-Only PPAV Source: Dependency Contract Review

31 October 2026. Independent automated source-contract review, not human
peer review, a reproof of the imported geometric algorithms, or geometric
or quantum execution. No new assumption mismatch was established for the
prime-only refinement. No novelty, hardness or speedup claim follows.

## Sources And Scope

Reviewed `bundles/prime-only-source-2026-10-25/PRIME_ONLY_SOURCE.md`,
`bundles/source-field-audit-2026-10-23/SOURCE_FIELD_AUDIT.md`, the joint
canonicalizer in `bundles/ppav-source-2026-10-23/PPAV_SOURCE_DECISION.md`,
and the size/clock argument in
`bundles/elliptic-theta-input-2026-10-26/UNIFORM_SOURCE_CLOCK.md`.

The retained full paper by Maria Corte-Real Santos, Etienne Piasecki and
Benjamin Wesolowski, [ePrint 2026/1142](https://eprint.iacr.org/2026/1142),
is the 44-page version at
`/Users/jaspersands/Developer/qsearch-research-work/ppav-source-2026-10-23/2026-1142.pdf`.
Its SHA256 was rechecked:
`4504310844c227e0d49c8c628b03e9942894f14fcd6f5881dc5c0122ed645318`.
Page references below are the printed page numbers of that version.

## Verified Imported Contracts

- **Efficiency:** A1, p10, bounds each routine's expected complexity by
  `input_length^poly(g)`. Fixed dimension 16 is essential; this is not a
  practical runtime bound or polynomial dependence on growing dimension.
- **Quotient:** A26, p14, accepts the complete `N^g`-point list of any
  maximal-isotropic subgroup of `X[N]`. Its output field is the smallest
  Frobenius-stability field of that subgroup. In the prime-only source,
  `N=r` at each call and the list has `r^16` points. The retained explicit
  small-prime bound makes this polynomial in the paid input length. The
  old even/nonfree prime-square issue is not part of this refined path.
- **Products:** A27 and Proposition 6.24, pp35--36, construct product
  theta-null coordinates by the Segre product and supply inclusions and
  projections.
- **Canonical models:** A7 is established by Lemma 6.22, pp34--35, through
  the finite symmetric theta-coordinate orbit and allowed two-torsion
  translations. Its bound is `input_length^poly(g)`.
- **Isomorphisms and automorphisms:** A22/A25 follow from Proposition 6.19
  and Corollary 6.20, pp33--34, enumerating the complete geometric
  isomorphism list. A8 supplies canonical point encodings. Use compatible,
  fixed field embeddings when invoking these statements.

The joint marking construction follows: move all levels by one isomorphism
to one canonical model; enumerate one shared automorphism on the entire
tuple; minimize each level's ordered tuple over its permitted common unit;
then minimize the concatenated tuple over that shared automorphism. A
different initial isomorphism merely permutes the same automorphism orbit.
Independent automorphism minimization at separate levels is not equivalent.

Theorem 6.25 is an **imported model theorem**. In particular, Proposition
6.24 calls A26 construction “trivial by construction”, although the atomic
isogeny encoding in Definition 6.1 already includes a codomain. Lemma 6.5
imports Lubicz--Robert 2012, Algorithm 4.10, for evaluation. This review
checked the stated interface and inspected these dependencies; it did not
reconstruct that quotient algorithm and its descent from first principles.
The observation is a review boundary, not a proved counterexample to A26.

## Field Argument Rechecked

The source contract pays for a common field defining the full source order
and the single isogeny. Frobenius commutes with that full quaternion order,
so it is an integer scalar `c=+/-p^m`; the target inherits the same scalar.
After one quadratic extension the scalar is `c^2=1 mod 8`. Every subsequent
prime-to-p quotient inherits this scalar Frobenius, and its full 8-torsion
is rational over the same base. Proposition 6.3, p26, uses rational
8-torsion for symmetric level-4 representability. Actual quotient
construction still uses A26, not representability alone.

For any geometric homomorphism between these objects, Frobenius naturality
and cancellation of the surjective scalar map show that the homomorphism
descends to the same base. Auxiliary prime-r points need an extension of
degree at most `r-1`. Use separate extensions with fixed embeddings.
Temporary fields during point evaluation must be descended back to the
fixed level field after each stage; carrying their compositum forward
would invalidate the resource argument. None of this grants a target
End/Hom lattice or a geometric ell-torsion basis.

## Existing Clock Argument Rechecked

The uniform-clock note gives an interface-size envelope independent of the
group query: fixed-dimension objects over one base, bounded per-level point
fields, polynomially many `r^16` kernel points, and additive-length flattened
morphism chains. These prevent repeated polynomial composition from causing
an unbounded growth of intermediate encodings. A1 then gives one uniform
expected polynomial bound `B(L)` for the complete label computation, with
all native evaluator costs included or paid in fixed preprocessing.

For this prime-ell source, `|Sp4(F_ell)|<ell^10`. Cap each always-correct
attempt at `2B(L)` and use

    h = ceil(10 log2(ell) + log2(1/delta))

independent tapes. Markov's inequality and a union bound imply that one
master tape, fixed before the quantum computation, produces the exact
canonical label at every group input except with probability at most
`delta`. No independence between different query inputs is needed. Bounded
reversible simulation, output copying and complete uncomputation then give
the conditional coherent oracle.

This transfer assumes always-correct successful outputs, as required by the
exact model interfaces; the paper does not separately spell out a complete
Las Vegas machine implementation. Wrong accepted labels cannot be repaired
by this timeout argument. The cited uniform-clock note is a theorem-level
composition, not an implemented dimension-16 circuit or numerical clock.

## Decision And Remaining Work

The prime-only refinement matches the reviewed formal PPAV contracts.
Keep imported Theorem 6.25, genuine common-field weak evaluations and paid
native evaluator bounds explicit. Missing execution alone is not a
mathematical falsifier, but arithmetic controls cannot certify the geometric
dependency or the end-to-end algorithm. The consequential remaining work is
the complete source/receiver and prior-art assessment plus the strongest
matched classical attack. This review requests no selector, geometric
backend, registry promotion or broader test campaign.
