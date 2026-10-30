# Surface Source Access Audit

2026-10-24. FOLLOW-UP SELF-AUDIT; NO NEW ALGORITHM OR INDEPENDENT REVIEW.

## Decision

The smooth repolarization proposal survives the specific access checks below.
That means no new counterexample was found, not that the geometric source has
been independently validated or executed. Its status remains
`PROPOSED_SOURCE_LEMMA_REVIEW_PENDING`. Do not promote a speedup or novelty claim.

This pass made no new scientific progress. It rechecked existing arguments and
rejected some tempting but unjustified classical shortcuts. Record that result
explicitly rather than calling another self-check a new theorem.

The authorized independent reviewer concerned the Rees proof, not this source.
That reviewer is finished. The earlier authorization does not authorize another
reviewer, and must not be represented as independent review of this construction.

## Actual Source And Dependency Chain

The source is the existing promised weak isogeny `phi:E^2 -> B`, with a full,
evaluable SOURCE order, the original polarized target model, a paid common
definition field, and common-unit weak auxiliary images for ONE global phi.
No target order, complete Hom module, hidden large-prime torsion, or new model
of an arbitrary polarization is an input.

The relevant successor notes are:

- `smooth-repolarization-2026-10-23/SMOOTH_REPOLARIZATION.md`;
- `prime-square-flags-2026-10-23/PRIME_SQUARE_FLAGS.md`;
- `kernel-output-2026-10-23/UNIFORM_SOURCE_BOUND.md`;
- `source-field-audit-2026-10-23/SOURCE_FIELD_AUDIT.md`;
- `ppav-source-2026-10-23/PPAV_SOURCE_DECISION.md`.

Do not use the older Desktop priority note as evidence that no converter has
been proposed, or that the PPAV framework paper is still unavailable.

## Checks Performed

1. The surface identity is genuinely quadratic: `S^2-t*S+I=0`, with S a positive
   quaternion-Hermitian TWO-by-two matrix of Moore determinant one. It does not
   apply unchanged in arbitrary dimension. The `t=2` branch must bypass the
   nonreduced formal quotient ring and use `H=I`.
2. The proposed quotient map has the correct direction:
   `F=H8^(-1)*C^dagger`, `F^dagger*H8*F=D^2*I`. Neither `C^dagger` alone nor
   an old-polarization interpolation of H supplies this map.
3. Non-free prime-square kernels remain covered by the two-stage isotropic
   flag proof. The shortcut `r*G` is not generally a Lagrangian first kernel.
4. The full source order and phi being defined over the SAME paid field imply
   scalar Frobenius on both endpoints. This is what makes arbitrary chosen
   flag subgroups descend; subgroup rationality alone does not suffice.
5. One quadratic base extension makes all 8-torsion rational on the scalar-
   Frobenius intermediates. Auxiliary torsion fields are still separate paid
   extensions with compatible embeddings, not an uncharged compositum.
6. Mark transport uses `q([D^-2] C Z)` on orders coprime to D. The uncomputed
   polarized isomorphism u is used only to prove the interpretation of these
   points. The evaluator does not need u or an inverse of q on arbitrary points.
7. Joint marked canonicalization must use one shared geometric isomorphism and
   automorphism across all levels. Independent per-level automorphisms, field
   Galois orbits, or independently rescaling individual basis points would
   change the equivalence relation.
8. The uniform trace bound and globally fixed auxiliary plan already exist.
   The fixed-random-tape argument remains conditional on uniform bounds and
   recognized success for the actual randomized routines. It is not a compiled
   source circuit, and the finite controls do not certify these implementations.

These are rechecks of the cited notes, not new deductions. No additional source
promise was silently introduced to make them pass.

## Classical Shortcuts Considered

The current mandatory attacks remain the direct source pullback, word-image
closure, and complete rank-one residual target-algebra test. See
`source-residual-algebra-2026-10-24/RESIDUAL_ALGEBRA.md`. They need actual paid
target maps; a symbolic element of the target rational algebra is not one.

An attractive next idea is to extract elliptic subvarieties from transported
source projections. If `e` is a source factor projection, the formal map
`T=phi*e*phi^dagger` obeys `T^2=ell*T`. However:

- Its image is an abstract elliptic subvariety, not automatically a compact
  model with an efficiently computable embedding.
- A compact evaluator for a map is not a polynomial-bit algorithm for
  factoring its image or connected kernel. Expanding a degree growing with
  ell is not polynomial in log ell.
- The PPAV decomposition primitive splits the GIVEN principal polarization.
  It does not find an arbitrary unpolarized product decomposition of B.
- Even an extracted image must be accompanied by a complete recovery argument
  for the SAME hidden kernel. Merely obtaining another representation of phi
  is not equivalent to recovering its large-prime kernel.

No effective extractor or complete new classical attack was found. Do not
implement these unproved conversions behind an innocuous helper function.
Conversely, their absence is not a classical lower bound or hardness evidence.

## Primary Literature Rechecked

The local 44-page version of Corte-Real Santos--Piasecki--Wesolowski,
[2026/1142](https://eprint.iacr.org/2026/1142), was read at complete pages 10-15
and 22-36. Its existing retained SHA256 is
`4504310844c227e0d49c8c628b03e9942894f14fcd6f5881dc5c0122ed645318`.
In particular, A26 explicitly includes a definition-field requirement; A7,
A22, and A25 concern already represented objects; A28 is polarized
decomposition. Importing the model theorem remains distinct from implementing
or independently proving all of those geometric algorithms.

[Chen et al., 2305.19897](https://arxiv.org/html/2305.19897), Definition 2 and
Theorem 1.1, concern elliptic weak isogeny representations and the established
hidden-Borel route. They are prior art, not a new mechanism discovered here.

[Montessinos, 2601.18050](https://arxiv.org/html/2601.18050v1), Sections 1.1-1.5
and Theorem 3.5, distinguishes unpolarized isomorphisms, IKO data, and full
effective/good endomorphism-ring representations. Those reductions do not
give an unpolarized decomposition from our weak data alone. In that paper,
"weakly known endomorphism ring" STILL supplies a basis of the entire ring;
it is not the weak-isogeny interface used here.

The existing comparison with [Page--Robert--Soumier,
2026/276](https://eprint.iacr.org/2026/276) likewise requires the full module,
not an unsaturated collection of transported maps. This pass revisited the
recorded input-contract audit and the public abstract; it did not independently
reprove the module-conversion theorem. These papers were already noted in the
smooth source bundle; rediscovering their titles is not new research progress.

## Next Decision

Do not repeat this access audit or add another adjacent arithmetic variant.
A useful next pass must supply one of:

1. An actual algorithm deriving a NEW target map or kernel information from
   the same indecomposable-target input, with every geometric operation paid.
2. A concrete new proof gap or constructive repair in the assembled source.
3. A properly scoped, external novelty/application comparison of the assembled
   result, or a pivot to another live research question if neither route yields
   a constructive step.

For integration, retain the separate statuses: proposed proof, finite algebraic
controls, imported geometric primitives, absent geometric execution, absent
coherent compilation, and unestablished novelty/separation. Do not ask Gemini
to fill a missing mathematical conversion with implementation scaffolding.

## Verification And Workspace Boundary

Focused source tests are rerun in separate processes to avoid isolated-module
name collisions. All 112 passed, with warnings as errors and no skips:

- smooth repolarization: 56 tests, 0.47 seconds;
- prime-square flags: 27 tests, 30.55 seconds;
- source fields: 18 tests, 0.37 seconds;
- uniform source bound: 11 tests, 1.54 seconds.

Each used `/opt/anaconda3/bin/python -m pytest -q -p no:cacheprovider -W error`
on its named test file, with bytecode and pytest plugin auto-loading disabled.
The retained PPAV PDF SHA256 was also recomputed and matched the record above.
These checks verify the existing algebraic and finite-field controls, not a geometric
backend. No code was changed, so repository-wide syntax/CLI/UI validation was
not claimed. The intended local checkout is still absent; source, staging,
central registries, Git, and migration state are untouched.
