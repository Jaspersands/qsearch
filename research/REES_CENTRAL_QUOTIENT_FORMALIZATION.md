# Actual Central Quotients And Class-Three Receiver Steps

27 October 2026. Scoped machine-checked algebra and channel identities for
the proposed Rees receiver. Not a new algorithm, complexity improvement,
novelty certificate, quantum execution, or proof of the whole receiver.

Follow-up: `REES_MEASURED_RECEIVER_FORMALIZATION.md` now connects the actual
complete central measurement to these sources, handles all records and
inactive targets, and proves the exact two-stage fresh-bank composition
conditional on total valid SDE policies. The remaining-gap statements
below describe this earlier quotient checkpoint.

## Scientific Question And Direction Choice

Can the class-three Rees receiver's central-descent interfaces be instantiated
by its ACTUAL successive quotients, for arbitrary nonnormal hidden H, without
assuming the quotient maps, hidden-image preservation, central weights, or
terminal recovery that the construction is supposed to establish?

The previous turn only revalidated Argon's already implemented requests:
NO NEW SCIENTIFIC PROGRESS. This pass first reread the existing unambiguous
decoder, Schur-locator, native norm-sampling and clock results. The putative
Gram-bound improvement was already established and attributed in those
notes. Changing auxiliary norm proposals is covered by the existing clock
falsifier; no new justified native sampler emerged from this examination.
That is not a new negative result or evidence of classical hardness.

The recent [two-fold multiplication paper](https://arxiv.org/abs/2610.00502)
remains a source of concrete plain-model codeword problems, but importing
its decoder again would not be research progress. Its randomly punctured
Reed--Muller regime is distinct from the already audited complete-AG regime;
the AG classical conclusions must not be applied to it without proof.

The Rees proposal remains a concrete end-to-end mechanism with identifiable
proof gaps. [Imran--Ivanyos](https://arxiv.org/abs/2304.08376) is the existing
bounded-prime central-conversion comparator. This pass does not rerun an
exhaustive novelty audit or infer novelty from a search returning no match.
The selected work removes a specific receiver premise rather than adding a
general-purpose research subsystem.

## Input, Mechanism, And Resource Scope

The original target is a finite Lie algebra L over the PRIME field F_p,
p>3, with class at most three, explicit public Lie coordinates and an
ordinary coherent oracle hiding arbitrary H in its BCH group. No hidden
generators, logarithmic subspace, grading of L, or hidden normality are
operational inputs. The existing prime-field subgroup correspondence derives
log(H)'s linearity; it is not extended to arbitrary extension fields.

The proposed receiver lifts to the positive lower-central Rees algebra,
uses cubic and quadratic central-character cancellation to descend, and
finishes with the additive coset state of all log(H). This pass constructs
the quotient groups and instantiates those two branchwise channel steps.
It does not improve the proposed polynomial-in-(dimension, log p) clock,
prove a classical lower bound, or supply a natural hard problem reduction.
Existing matrix, code and polynomial stabilizer filters retain their
individual promises and resource charges.

SDE witnesses, independent source tensors and nonzero branch traces are
still inputs to the formal channel theorems. The positive-branch condition
is exactly on the defined projected source, not on guessed character
statistics. Complete spectral instruments, coherent gate synthesis,
fresh-source recursion, solver success/runtime and total receiver error
accounting are not certified by this pass. Finite source types are proved;
their noncomputable `Fintype` descriptions are not efficient enumeration
algorithms or extracted quantum circuits.

## Actual Quotients

`formal/Formal/ReesCentralQuotient.lean` constructs the actual ideals

    F_{>d} = {a in A : coefficient_r(a)=0 for every r<=d}

and the Mathlib Lie quotients `Trunc d = A / F_{>d}`. Positive polynomial
degrees prove bracket closure, class at most d, and centrality of the
kernel of `Trunc(d+1) -> Trunc d`. No supplied bracket table or centrality
interface replaces these facts.

The top kernel is exactly the injective image of `gamma_(d+1)(L)` under
`v -> class(t^(d+1) v)`. Substitution by u acts there by u^(d+1).
Retained coefficients inject the quotient into a finite product of L;
finiteness does not assume the infinite current algebra is finite.
At a proved class bound the tail ideal is zero, identifying the full
truncation with the original untruncated Rees algebra.

`formal/Formal/ReesCentralQuotientBCH.lean` uses the previously proved
cubic BCH group to construct actual projection homomorphisms. Its kernel
is central, equals the central coefficient embedding's range, and gives
the expected group quotient by the first isomorphism theorem. The full
degree-three group is equivalent to the original Rees group.

Hidden subgroups at every level are actual images under these maps.
Their dilation invariance is derived from invariance of the lifted H.
The degree-one group is isomorphic to ADDITIVE L, not the original
nonabelian BCH group on L or the abelianization L/[L,L]. The terminal
hidden image is exactly the logarithm set of the original arbitrary H.

## Derived Channel Obligations

`formal/Formal/CentralQuotientReceiver.lean` proves:

* A disallowed character has an identically zero projected source matrix.
  Nonzero trace is equivalent to being trivial on `embed^-1(H)`.
* For an actual quotient with kernel `image(embed)`, support membership is
  exactly membership in the image of H, without H containing that kernel.
* Subgroup-preserving automorphisms with the specified central action
  preserve the saturation HZ. Their supported correlations and phase
  product are derived, not postulated.
* The controlled-discard channel on an independent normalized tensor gives
  precisely the quotient coset matrix, for ANY right-inverse section.
* The vector SDE implies character cancellation on EVERY central element.
  Dropping zero scales preserves this equation at positive degree, and a
  nonzero witness supplies a nonempty active tensor.

`formal/Formal/ReesClassThreeReceiver.lean` instantiates these obligations
with the concrete Rees groups, embeddings, dilations and hidden images.
Its `degree_three_output` and `degree_two_output` use explicit coefficient
sections: retain lower coefficients and insert a zero top coefficient.
The sections are not supplied as efficient-oracle assumptions and are not
asserted to be homomorphisms. H does not appear in their definitions.

Finally `terminal_source` relabels the actual degree-one quotient matrix:

    rho(x,y) = 1/|L| if BCH.mk(y-x) belongs to H, else 0.

This formalizes preservation of ALL of log(H), including derived directions.
It is a source identity, not an implemented Fourier readout or complete
recursive preparation theorem.

## Decisive Controls

`tests/test_central_quotient_receiver.py` uses UT3(F_3) x F_3 with
H={(a,0,c,c)}. H is nonnormal and meets its two-dimensional center in a
proper one-dimensional subgroup. Direct matrix calculations check all nine
character projectors, all zero and nonzero projected sources, and quotient
outputs for both a simple and a nonlinear non-homomorphic section.

The three admissible labels have probability 1/3, not 1/9. Retaining the
old transverse normalization produces output trace NINE after two targets;
proper normalization gives trace one and the correct quotient coset matrix.
These are bounded arithmetic controls, not generated oracle candidates or
empirical speedup claims. Existing class-three finite-instrument tests are
retained as a separate implementation cross-check. The F_3 fixture tests
the generic central-quotient identity, not the p>3 cubic BCH construction.

An additional control sets the base character to the trivial character.
All nine linear labels then repeat the same projector; their sum is not
identity and their apparent outcome masses sum to three. The branchwise
theorems allow arbitrary base characters, but a complete linear-label
spectral instrument on a nontrivial center requires a nontrivial one.

## Independent Semantic Review

One independent read-only reasoning agent inspected all four new modules,
the concrete corollaries and the existing prime-field correspondence. It
found no semantic defect or target conclusion hidden as a premise. It
specifically checked actual versus truncated covers, finite-coordinate
finiteness, arbitrary H, central weights, normalization, non-homomorphic
sections, H-independent controls and retention of all log(H).

It emphasized the nontrivial-character requirement for a later complete
instrument and the remaining source/solver/recursion obligations. That
qualification is retained above. This was automated review, not human
specialist validation, a novelty certificate, or an independent test run.
The parent read both delegated implementation modules and all review findings.

## Verification And Changed Files

Fresh verification after final proof integration:

* Full default Lean build: PASS, 3494 jobs including cached dependencies.
* Strict checks on all four new modules and `Formal/Audit.lean`: PASS,
  with warnings as errors, `autoImplicit=false` and
  `relaxedAutoImplicit=false`.
* 44 new local headline axiom guards are repeated in the global audit.
  They allow only subsets of `propext`, `Classical.choice`, `Quot.sound`.
* Eight selected Python files: 128 tests PASS in 8.97 seconds, including
  four new cases. This is not a full-repository Python-suite result.
* New Python test syntax: PASS. `qsearch.py validate`: `valid=true`,
  `issues=[]`. No registry promotion or new speedup claim.
* `git diff --check`: PASS after removing a trailing blank line in the
  global audit. No proof statement changed in that cleanup.
* No JavaScript changed; no JavaScript check was needed or claimed here.

From `formal/`, using the installed pinned Lean 4.35.0 toolchain:

```text
lake --no-cache build --wfail
lake --no-cache env lean -DwarningAsError=true -DautoImplicit=false -DrelaxedAutoImplicit=false Formal/CentralQuotientReceiver.lean
lake --no-cache env lean -DwarningAsError=true -DautoImplicit=false -DrelaxedAutoImplicit=false Formal/ReesCentralQuotient.lean
lake --no-cache env lean -DwarningAsError=true -DautoImplicit=false -DrelaxedAutoImplicit=false Formal/ReesCentralQuotientBCH.lean
lake --no-cache env lean -DwarningAsError=true -DautoImplicit=false -DrelaxedAutoImplicit=false Formal/ReesClassThreeReceiver.lean
lake --no-cache env lean -DwarningAsError=true -DautoImplicit=false -DrelaxedAutoImplicit=false Formal/Audit.lean
```

From the repository root, the Python interpreter was
`/opt/anaconda3/bin/python`. `PYTHONPYCACHEPREFIX` was set to
`/tmp/qsearch-central-quotient-pycache` for these checks:

```text
env PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /opt/anaconda3/bin/python -m pytest -q -p no:cacheprovider -W error tests/test_central_quotient_receiver.py tests/test_rees_review_controls.py tests/test_rees_hsp_reduction.py tests/test_uniform_bch_rees.py tests/test_rees_complete_instrument.py tests/test_rees_copy_only_outer.py tests/test_central_character_descent.py tests/test_prime_power_rees_descent.py
/opt/anaconda3/bin/python -m py_compile tests/test_central_quotient_receiver.py
/opt/anaconda3/bin/python qsearch.py validate
```

New code files are the four Lean modules named above and
`tests/test_central_quotient_receiver.py`. Default imports and global guards
changed in `formal/Formal.lean` and `formal/Formal/Audit.lean`. Documentation
changes are this note, `formal/README.md`, `research/AGENT_HANDOFF.md`,
the current formal-status paragraph in `research/REES_HSP_REDUCTION.md`,
a follow-up pointer in `research/REES_CLASS_THREE_GROUP_FORMALIZATION.md`,
and the external working checkpoint. Existing unrelated dirty changes,
Argon's review and historical verification evidence were preserved.

Verified source SHA-256 values:

```text
4d6c2483e398989c8aecc18f711e07308f2cf1a422abd9aa464fd0c08d52d50b  formal/Formal/CentralQuotientReceiver.lean
7a075d81dc6c2c1329242da56ba34fd02f466b483361bbc6f453ea58ba0586ba  formal/Formal/ReesCentralQuotient.lean
1a4f1609dae86e84fe282c8bdeb771f5d366888d71000b8d0362959e137f4bf1  formal/Formal/ReesCentralQuotientBCH.lean
16023939900028f79ec2332cb73b475a19d5cc534e1b712f382d32e013a6f2ea  formal/Formal/ReesClassThreeReceiver.lean
884905b38705416dbc5fe85b755291c47fbb0a0aa5bfc3c49b5c7f4406480b98  formal/Formal.lean
3dd2ba5bd781ec60efc036619822e30c8b3a3bc6dd095221569b833742579203  formal/Formal/Audit.lean
2083b91ea70b4d2ffdfb1e5948cce5f0a6cf8701948c36d38025a5d45dca4528  tests/test_central_quotient_receiver.py
```

## Remaining Falsifiers And Next Decision

The channel result fails without independent conditioned sources, an actual
central quotient, both-direction hidden-image preservation, a nonempty
active bank, or the full vector cancellation equation. Non-homomorphic
sections and nontrivial H-intersections are handled, not excluded.

The next receiver gap is the complete restored spectral instrument and
its connection to all-record fresh-source recursion, followed by solver
and clock verification. General-class and prime-power-ring BCH also remain
outside the proved group layer. A separately implemented classical section
or density-matrix emulator is not a quantum implementation.

Before another formal pass, compare that obligation with a concrete new
native-source mechanism. Do not repeat the now-closed quotient, central
weight, or terminal-retention premises as new progress. There remains no
demonstrated Shor-level application or verified classical hardness.
