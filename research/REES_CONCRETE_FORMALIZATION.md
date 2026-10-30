# Concrete Rees Algebra And Prime-Power Interpolation

27 October 2026. Formal proof work on specific obligations of the proposed
Rees HSP theorem, not a new quantum algorithm, a novelty certificate, or a
formal verification of the entire receiver. Validation is recorded below
only after the relevant commands finish.

Later follow-up: `REES_CLASS_THREE_GROUP_FORMALIZATION.md` now supplies
actual BCH groups and the concrete evaluation/group-hiding bridge at class
at most three. The remaining-scope statements and hashes below describe
this earlier Lie-level checkpoint, not that later group-layer pass.

## Why This Pass

The preceding review integration was revalidated; repeating those checks
did not add an algorithmic result. This pass first compared the remaining
constructive directions using current repository and external checkpoint
files:

- The inverse-trace problem already has an ideal quantum construction,
  accepted-flat and subfield classical attacks, an exact residual SAT
  interface, and detailed norm/repair audits. Prime-degree general search
  is unresolved. No new scalable solver emerged from the parent's search;
  failed attacks are not hardness evidence.
- The fixed-field AG norm proposal has a proved rejection-clock limitation.
  More auxiliary-code or multiplier choices within that proposal do not
  resolve native search. Approximate counting is already classically easy
  under its stated distance promise.
- The Rees HSP proposal has an actual end-to-end mathematical mechanism,
  but its existing Lean interpolation theorem assumed the evaluation
  homomorphisms. Closing the concrete algebraic part of that assumption is
  more valuable than another finite example or adjacent attack barrier.

The scientific question is whether the positive lower-central cover and
its evaluation maps can be derived from the actual Lie axioms, without
silently truncating a bracket or assuming the original algebra is graded.
The separate prime-power interpolation obligation must work over a ring
with zero divisors and a possibly nonfree quotient.

One independent reasoning reviewer checked the inverse-trace resampling,
polynomial-interpolation and algebraic-coding alternatives. It found no
new solver or public key equation. Ordinary interpolation of accepted
values at N-K coordinates still leaves K predicates and success factor
lambda_b * 2^(-K), rather than a polynomial algorithm. This corroborates
the choice not to run another seed or SAT-budget campaign; it is not a
new classical lower bound. The reviewer is closed.

## Ring Interpolation

`formal/Formal/ReesHomogenization.lean` now defines its row operations and
evaluation matrix over an arbitrary commutative ring. The old field
theorems are specializations, not duplicate proofs.

`coefficientwise_iff_of_isUnit` proves that membership of all evaluations
in any submodule is equivalent to coefficientwise membership whenever the
evaluation determinant is a UNIT. Its proof uses the actual matrix inverse.
There is no free-module premise on the coefficient module or its quotient.
`tuple_hides_of_isUnit` carries this to the original ordered oracle tuple,
with the same explicit group-homomorphism and log/coefficient premises as
the existing field interface.

`formal/Formal/ReesPrimePowerInterpolation.lean` supplies the missing
arithmetic specialization. For prime p, e>0 and c<p, the public points
1,...,c and all their positive differences are units modulo p^e. Therefore

    det(V) = product_i s_i * product_(i<j) (s_j-s_i)

is a unit. Its `coefficientwise_iff` and `tuple_hides` theorems apply to any
module and submodule over Z/(p^e). All prime-power exponents are covered;
this is not a finite numerical check.

The negative control is kernel-checked too. Over Z/9, points 1 and 4 are
distinct units, and the evaluation determinant is 3: nonzero but not a
unit. The coefficient vector (6,3) is nonzero, while 6t+3t^2 vanishes at
both points. Distinctness or a nonzero determinant alone cannot justify
ring interpolation. This is not a counterexample to the manuscript,
whose canonical point choice satisfies the stronger condition.

## Concrete Lie Construction

`formal/Formal/ReesLieConstruction.lean` constructs the cover in the
ordinary current Lie algebra `AddMonoidAlgebra R Nat` tensor `L`. The
coefficient ring is any commutative ring. The proof uses actual Lie axioms
and the actual lower central series, not an assumed positive grading.

1. Jacobi and span induction prove `[gamma_r,gamma_s] <= gamma_(r+s)`.
2. The positive lower-central monomials span an actual Lie subalgebra.
   Its coefficient characterization excludes a constant term and exactly
   identifies the coefficient at r with gamma_r(L).
3. If gamma_(c+1)=0, every coefficient above c is zero. A homogeneous
   bracket whose degree exceeds c is zero in the UNTRUNCATED current
   algebra. A separate theorem proves the cover's class is at most c.
4. Evaluation is an actual Lie homomorphism. Substitution t -> a*t is an
   actual Lie endomorphism; if a is a unit it is a Lie automorphism.
5. The grade-one map retains all L and is split by evaluation at one.
   This is a LINEAR section, not a Lie section: brackets land in grade two.

A delegated proof implementation supplied this module. The parent read
the complete proof and independently compiled it before integration. Its
12 local axiom guards use only standard Lean axioms. The agent is closed.

## Actual Hidden-Cover Bridge

The parent implemented `formal/Formal/ReesLieInterpolation.lean` to connect
the new construction to the existing interpolation proof. This is not
merely a second unconnected interface.

The proved cutoff converts the actual finitely supported evaluation sum
to the finite matrix expression with coefficients 1,...,c. For an arbitrary
Lie subalgebra h of L, define the hidden cover as the intersection of the
preimages of h under the actual evaluation maps. This is an actual Lie
subalgebra, whether or not h is an ideal or homogeneous. Invertible
interpolation proves it is exactly the set of currents whose positive
coefficients lie in h intersect gamma_r(L). The intersection uses the
AMBIENT lower central series, not h's own lower central series.

The scaling formula then proves invariance under every scalar in one
direction and under every unit in both directions. The prime-power
specialization supplies the canonical interpolation points and their unit
determinant. The hidden h appears only in the correctness predicate;
neither operational evaluation nor dilation takes h as an argument.

## Remaining Boundary

No group-level evaluation homomorphism is obtained merely by proving a
Lie-level one. The universal BCH/Lazard identification and its functoriality
must still be connected in Lean. The full central-character instrument,
all-label distribution, recursive adaptive error budget, SDE implementation
and runtime, and native source/application obligations remain separate.
The module definitions are noncomputable mathematical objects, not
extracted algorithms or a formal refinement of the Python implementation.
No finite-dimensional rank or gate-count theorem has been added.

The published scalar and fixed-degree SDE dependency was rechecked against
[Ivanyos--Santha](https://arxiv.org/html/1503.09016v2), Fact 2 and Section 3.
Its deterministic general construction must not be confused with the
random-nonresidue quadratic/cubic warm-ups. No new SDE result is claimed.

The current goal remains active. No candidate status, novelty claim,
classical-hardness claim or quantum-speedup claim is promoted by this pass.

## Verification

All checks below completed. Both agents used in this pass are closed, and
all verification processes started here have finished.
From `formal/`, with the pinned Lean 4.35.0 `lake` executable:

```text
lake --no-cache build --wfail
lake --no-cache env lean -DwarningAsError=true -DautoImplicit=false -DrelaxedAutoImplicit=false Formal/ReesHomogenization.lean
lake --no-cache env lean -DwarningAsError=true -DautoImplicit=false -DrelaxedAutoImplicit=false Formal/ReesPrimePowerInterpolation.lean
lake --no-cache env lean -DwarningAsError=true -DautoImplicit=false -DrelaxedAutoImplicit=false Formal/ReesLieConstruction.lean
lake --no-cache env lean -DwarningAsError=true -DautoImplicit=false -DrelaxedAutoImplicit=false Formal/ReesLieInterpolation.lean
lake --no-cache env lean -DwarningAsError=true -DautoImplicit=false -DrelaxedAutoImplicit=false Formal/Audit.lean
```

The complete build passed with 3487 jobs, including cached dependencies.
This is not a count of new proofs. All five strict individual checks passed.
The default build imports all three new modules. Thirty new global axiom
guards cover the ring interface, concrete construction, bridge and negative
controls, with only `propext`, `Classical.choice`, and `Quot.sound` allowed.

From the repository root:

```text
env PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONPYCACHEPREFIX=/tmp/qsearch-rees-concrete-pycache /opt/anaconda3/bin/python -m pytest -q -p no:cacheprovider -W error tests/test_rees_review_controls.py tests/test_rees_hsp_reduction.py tests/test_uniform_bch_rees.py tests/test_rees_complete_instrument.py tests/test_rees_copy_only_outer.py tests/test_central_character_descent.py tests/test_prime_power_rees_descent.py tests/test_norm_sampler_clock.py
```

**152 selected Python tests passed in 10.28 seconds.** This includes the
previous norm-clock tests as a checkpoint regression; no Python algorithm
was changed in this pass. It is not the entire Python repository suite.
Syntax checks passed for the seven selected theorem/test Python files.
`python qsearch.py validate` returned `valid: true`, `issues: []`, with
8 candidates, 796 experiments, 807 results and 973 negative results.
`git diff --check` passed.

The historical `node --check index.js` command failed because that root
file no longer exists. The actual twelve JavaScript files under `site/js/`
were then located and each passed `node --check`. No UI file was edited.
No manuscript edit or new LaTeX compilation is claimed in this pass.

Final formal-source SHA-256 values for this checkpoint:

```text
f9459f4c9e46512f089c9478985576ccbb243c4640d2594130bdf182ba3a6634  Formal/ReesHomogenization.lean
f29beee234832c43d815ff923a50d5f432b25f210bd42b41129305d5359c434a  Formal/ReesLieConstruction.lean
3d78966f0a7af4137f3a3fa65631f006a970f366cdb7ead44af57595cd4e6fd4  Formal/ReesPrimePowerInterpolation.lean
b42621af1b397949c375f68e1c23cad0e1a7e4cf7a620b5ea2b351308556bdb3  Formal/ReesLieInterpolation.lean
53b5b6e6118a3e1b01c5c44afcac0619ac13fd4c9dbf37d6a37f2f04f47cc3eb  Formal/Audit.lean
```

The earlier Argon-disposition hashes describe the previous interface
checkpoint, not these later sources. That historical record is preserved.

## Changed Files And Next Question

This pass adds `ReesLieConstruction.lean`, `ReesLieInterpolation.lean`,
`ReesPrimePowerInterpolation.lean`, and this note. It updates
`ReesHomogenization.lean`, the default imports, the global axiom audit,
`formal/README.md`, `REES_HSP_REDUCTION.md`, and the research handoffs.
No CLI command, registry admission, dependency installation, UI change,
commit, push or external contact was performed.

The next proof obligation is an actual BCH/Lazard transport into the
group-level tuple interface, not more interpolation fixtures. Its expected
value should be compared with finding a useful native source for the Rees
theorem before committing to a full formalization campaign. The native
inverse-trace residual remains open; neither this proof work nor the
reviewer's unsuccessful attack supplies a hardness claim or a new solver.
