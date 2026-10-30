# Actual Class-Three Rees Group Transport

27 October 2026. Formal verification of specified algebraic obligations,
not a new BCH identity, a new algorithm, a novelty certificate, or a proof
of the complete Rees quantum receiver. Argon's original review is unchanged.

Follow-up: `REES_CENTRAL_QUOTIENT_FORMALIZATION.md` now constructs the actual
successive quotients and instantiates the class-three branchwise receiver
steps. The verification and remaining-gap statements below describe this
earlier group-transport checkpoint, not the follow-up's additional coverage.

## Research Decision

The preceding pass checked the actual positive lower-central Lie cover,
but the tuple-hiding theorem still required group homomorphisms as inputs.
A Lie homomorphism alone did not discharge those premises. This pass
constructs the group and its maps in the first class beyond the published
nil-2 regime, rather than assuming a Lazard transport interface.

Before choosing this obligation, the existing logical-gate, projective-state,
quadratic-form and succinct-polynomial application audits were reread. None
supplies a demonstrated useful hard native input. The rank-one quadratic
probe leads to a dihedral rather than nilpotent subgroup problem; the
state route needs a global gap; the polynomial route must survive its
white-box classical filters. These are scoped existing findings, not new
negative results or impossibility theorems.

Argon's random-column SDE suggestion remains an open algorithmic question.
The [published diagonal-system algorithm](https://arxiv.org/abs/1503.09016)
already gives polynomial time at fixed degree with a sufficiently large
number of variables. No faster constructive algorithm for the required
random-label model was established in this pass. Existence, random rank,
or a small numerical example would not justify a smaller receiver clock.

## Checked Group Construction

`formal/Formal/BCHClassThree.lean` defines the actual multiplication

```text
x * y = x + y + [x,y]/2 + ([x,[x,y]] + [y,[y,x]])/12.
```

Its premises are genuine Mathlib Lie axioms over a field F,
`lowerCentralSeries F L L 3 = bottom`, and nonzero 2 and 3 in F. In
particular, it includes prime fields of characteristic greater than three;
it does not impose characteristic zero or an original grading.

The lower-central hypothesis implies every length-four right-nested bracket
vanishes. Jacobi, bilinearity and scalar arithmetic then prove associativity.
The identity is zero and the inverse is negation. These facts instantiate
a `Group` on the separate `BCH F L hnil` carrier; associativity is not an
input premise disguised as a typeclass.

Every actual Lie homomorphism induces a group homomorphism (`lieHom`),
and every Lie equivalence induces a group equivalence (`lieEquiv`).
`val_pow` and `val_zpow` identify group powers with scalar multiples of
their logarithms. The module proves its formulas in Lean; it does not
extract a circuit or certify that a Python routine implements them.

## Concrete Rees Composition

`formal/Formal/ReesGroupClassThree.lean` applies this construction to
the actual `rees` Lie algebra, using its already proved class bound.

* `evaluationHom` comes from actual polynomial-current evaluation.
* `evaluation_identity` proves its finite coefficient formula.
* `subgroupOfLie` proves a Lie subalgebra is closed under the actual group law.
* `hiddenSubgroup` uses the actual intersection of evaluation preimages.
* `tuple_hides` and `tuple_hides_subgroup` instantiate the older hiding
  interface. Neither assumes evaluation homomorphisms or their coefficient
  identity as separate inputs.
* `dilationEquiv` is an actual group automorphism; `dilation_hidden_iff`
  proves both directions of hidden-subgroup preservation.
* `canonicalPoints = (1,2,3)` has evaluation determinant 12, proved to be
  a unit under the same field characteristic hypotheses.

The hidden Lie subalgebra need not be an ideal or homogeneous, and is a
correctness parameter rather than an input to evaluation or dilation.
The coefficient relation is for `log(a^-1*b)`, not `log(b)-log(a)`.
Grade-one retention remains a linear statement, not a group section.

## Checked Prime-Field Subgroup Correspondence

`formal/Formal/BCHClassThreeSubgroups.lean` derives a Lie subalgebra from
an ARBITRARY subgroup H of the prime-field BCH group, without assuming
logarithmic linearity. `toLieSubalgebra` has exactly the carrier
`{x : BCH.mk x belongs to H}`. The reverse `toSubgroup` construction and
both round-trip equalities are proved. There is no normality, transversality,
grading, finite-generation or supplied-generator premise on H.

This correspondence is not asserted over an arbitrary coefficient field:
even additive subgroups need not be linear over a field extension, and
integer lattices need not be rational subspaces in characteristic zero.

Over the prime field, scalar multiples are ordinary powers. The exact
reconstruction words proved in Lean are as follows. Let
`C = log(exp(x) exp(y) exp(-x) exp(-y))`, and let A and B be the logarithms
of the commutators of exp(x), respectively exp(y), with that commutator.
Then

```text
C = [x,y] + ([x,[x,y]] + [y,[x,y]])/2,
A = [x,[x,y]],  B = [y,[x,y]],
log(exp(C) exp(-(A+B)/2)) = [x,y],
log(exp(x) exp(y) exp(-[x,y]/2) exp(A/6) exp(B/3)) = x+y.
```

The A and B terms are central. These words avoid circularly assuming
addition or bracket closure of the hidden subgroup. Exact symbolic UT4
controls independently check the orientation and coefficients; the universal
implication is supplied by the Lean proof, not by these matrix controls.

The parent bridge now has `tuple_hides_arbitrary_subgroup`, using the
canonical points 1,2,3 and the original oracle relation for ANY subgroup H.
The evaluation/group maps, their coefficient identity, and log(H)'s Lie
closure are all constructed or proved, not assumed. `lifted_mem_coefficients`
characterizes the lifted subgroup directly by membership of the original
coefficient exponentials in H. `dilation_arbitrary_subgroup` proves its
invariance under every unit dilation. The hidden H is still only a
correctness parameter; it is not supplied to the public maps.

These are mathematical power words, not an extracted polynomial-time
implementation or a formal complexity proof for repeated squaring.

## Decisive Controls And Remaining Scope

Three additional controls are in `tests/test_rees_review_controls.py`:

1. Quadratic truncation at class three has associator `-E03/4` for
   `x=E01+E12`, `y=E23`, `z=E01` in strictly upper-triangular 4x4 matrices.
2. Cubic truncation at class four has associator `-E04/24` for
   `x=E01`, `y=E12`, `z=E23+E34` in 5x5 matrices.
3. The bracket and addition reconstruction words above are checked on
   symbolic, not sampled, upper-triangular 4x4 inputs.

The class bound and cubic terms cannot be omitted. The new group layer is
not a proof for arbitrary fixed class or for prime-power coefficient rings.
The separately checked ring interpolation theorem does not fill that gap.
Full spectral instruments, recursive quotient transport, fresh-source
induction, solver clocks, quantum implementations and total runtime remain
outside this group-layer formalization. No hardness or speedup claim follows.

## Verification

All checks below completed successfully. The pinned executable was
`/Users/jaspersands/.elan/toolchains/leanprover--lean4---v4.35.0/bin/lake`.
From `formal/`:

```text
lake --no-cache build --wfail
lake --no-cache env lean -DwarningAsError=true -DautoImplicit=false -DrelaxedAutoImplicit=false Formal/BCHClassThree.lean
lake --no-cache env lean -DwarningAsError=true -DautoImplicit=false -DrelaxedAutoImplicit=false Formal/BCHClassThreeSubgroups.lean
lake --no-cache env lean -DwarningAsError=true -DautoImplicit=false -DrelaxedAutoImplicit=false Formal/ReesGroupClassThree.lean
lake --no-cache env lean -DwarningAsError=true -DautoImplicit=false -DrelaxedAutoImplicit=false Formal/Audit.lean
```

Default build: **3490 jobs, including cached dependencies**, not 3490 new
proofs. There are **31 new global axiom guards**, in addition to local
guards, permitting only subsets of `propext`, `Classical.choice` and
`Quot.sound`. The parent read all new proofs and repeated the build and
strict checks. One delegated implementer supplied the two BCH modules;
that agent is closed. This was not a separate human or independent
specialist review.

From the repository root:

```text
env PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONPYCACHEPREFIX=/tmp/qsearch-bch3-pycache /opt/anaconda3/bin/python -m pytest -q -p no:cacheprovider -W error tests/test_rees_review_controls.py tests/test_rees_hsp_reduction.py tests/test_uniform_bch_rees.py tests/test_rees_complete_instrument.py tests/test_rees_copy_only_outer.py tests/test_central_character_descent.py tests/test_prime_power_rees_descent.py tests/test_norm_sampler_clock.py
env PYTHONPYCACHEPREFIX=/tmp/qsearch-bch3-pycache /opt/anaconda3/bin/python -m py_compile tests/test_rees_review_controls.py
env PYTHONPYCACHEPREFIX=/tmp/qsearch-bch3-pycache /opt/anaconda3/bin/python qsearch.py validate
git diff --check
```

**155 selected Python tests passed in 9.12 seconds**, including three new
controls. This is not the entire repository Python suite. Syntax and
registry validation pass (`valid: true`, `issues: []`; 8 candidates,
796 experiments, 807 results, 973 negatives). All 12 actual JavaScript
files under `site/js/` also pass `node --check`; no root `index.js` exists
and no UI code changed. No registry status was promoted.

Final source fingerprints:

```text
d8c026fb5b10bdc2cc906fdee0e91373aef46959357def819e5435df7a30363d  Formal/BCHClassThree.lean
bb7e1dfad2c7f310c1ed6902c4ab6836ed30ce538e5a652dfc6caad3d5c3e454  Formal/BCHClassThreeSubgroups.lean
e512991588bdfcd4a4e834642c81e76e61bf79e70d2a779684c0eadcd1edae30  Formal/ReesGroupClassThree.lean
3bf4af1b055d72b6c8380d00cd4b0ae76f032fed261e258382b113207f2ce985  Formal/Audit.lean
2c1f72fc3d92b72341a9ea70d9178560c04ac0ca57ee4c935ffb8e1664bc2014  tests/test_rees_review_controls.py
```

## Changed Files And Next Decision

The three new Lean modules above, their default imports and global audit;
the three additional controls in `tests/test_rees_review_controls.py`;
this note, `formal/README.md`, the preceding formalization checkpoint,
`REES_HSP_REDUCTION.md`, the review brief and the research handoffs changed.
The original Argon review and manuscript are unchanged in this pass.
There was no commit, push, external contact, dependency update or migration.

The next receiver-specific proof gap is the actual graded central subgroup
and quotient instrument/recursion, not this now-closed class-three
group-transport premise. Recompare that proof work with a genuinely useful
native-source construction before extending the formalization by inertia.
The overall discovery goal remains ACTIVE; this is proof progress, not an
algorithmic speedup or a demonstrated hard application.
