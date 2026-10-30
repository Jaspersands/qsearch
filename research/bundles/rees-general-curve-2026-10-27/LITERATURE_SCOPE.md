# Source-Extension Prior-Art Boundary

2026-10-27. Bounded primary-source check, not an exhaustive novelty search.
The full receiver prior-art review remains the separate
`../rees-novelty-recheck-2026-10-27/REVIEW.md`.

## Imported Mathematics

- Nonsingular finite-field fiber counting: Bafna, Sudan, Velusamy and Xiang,
  [arXiv2102.00602v1, Corollary 1.3](https://arxiv.org/html/2102.00602v1).
  This applies to nonsingular roots without assuming the full fiber finite.
- Complex irreducible degrees in a finite p-group: the nilpotent-group
  induction theorem in [Teleman's notes, Theorem17.5](https://www.math.uchicago.edu/~margalit/repthy/RepThry.pdf)
  yields powers of p and hence dimension at least p for nonlinear blocks.
- Finite-group Plancherel and the representation-dimension flattening
  mechanism are standard. [Tao's discussion](https://terrytao.wordpress.com/2011/12/16/254b-notes-3-quasirandom-groups-expansion-and-selbergs-316-theorem/)
  is conceptual background, not a theorem that these groups have no
  low-dimensional nontrivial representations. They have linear characters.
- The polynomial character-sum bound, BCH identities, finite-field
  polynomial zero bound and weighted free Lie construction are standard
  ingredients. We do not claim them as research discoveries.

The general weighted-curve argument is an application/composition of these
ingredients. This search did not certify its novelty. Broad search also
found [Ionescu et al., arXiv2112.03322](https://arxiv.org/abs/2112.03322),
but its abstract concerns ergodic averages in discrete step-two nilpotent
groups. That is not an exact match to the present finite-field singular-
value statement; no claim about the entire paper's coverage is made.

## Existing StateHSP Coverage

[Hinsche, Eisert and Carrasco, arXiv2505.15770v3](https://arxiv.org/html/2505.15770v3)
already solve abelian StateHSP and connect it to stabilizer, cut and
translation-symmetry learning. Their Definition1 has pointwise overlap
separation. The present work must not promote its abelian special cases or
those applications as newly discovered tasks.

[Liu et al., arXiv2609.35656v1](https://arxiv.org/html/2609.35656v1)
distinguish copies from preparation/inverse access and establish optimal
abelian copy/query gap dependence. The new source keeps copy-only native
state access plus paid coherent group action. It neither grants a state
preparation inverse nor improves their optimal abelian bounds. Their
abstract and the existing repository scope audit were rechecked; a full
independent reproof of their lower bounds was not performed.

[Holt and Subramanian, arXiv2609.38085v2](https://arxiv.org/html/2609.38085v2)
address nonabelian normal-core learning, ray symmetries, coding-based
linearisation, and reductions for other quantum objects. The local
`REES_PROJECTIVE_STATE_SOURCE.md` already compares its linear-action Rees
evaluation homomorphisms to that paper. This pass changes the state-gap
promise at fixed class, not that paper's projective-representation scope.
The title/abstract and prior local audit were checked here, not every
theorem in the paper again. General Hamiltonian/unitary symmetry reductions
are therefore not an unoccupied new application category by themselves.

## Research Decision

Keep the general-c source extension as a scoped mathematical tool, now with
one independent AI mathematical review. Do not admit another algorithmic-advantage candidate
merely because its proof and public algebra controls pass.

A valuable next proposal must supply a concrete motivated task with:

1. A uniform explicit action of genuinely relevant higher-class scope.
2. Native acquisition and coherent-action costs, including state width.
3. A proved inverse-polynomial subgroup-twirl robustness promise.
4. An explicit output that existing abelian/normal-core learners do not
   already recover, or a proved cost improvement against their actual
   assumptions. A nonnormal subgroup alone is not evidence of hardness.
5. A matched comparator: quantum-input data cannot silently become a
   polynomial-size classical amplitude table. Conversely, a supplied
   classical description must be available to the classical algorithm.

The decisive falsifier is an already efficient learner or classical
description-based procedure for the SAME task. Do not generate planted
StateHSP instances merely to populate the registry. No new task meeting
all five conditions is established in this pass.
