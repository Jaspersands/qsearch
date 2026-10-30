# Handoff: Frobenius-Power Completion

## Research Result

Read FROBENIUS_COMPLETION.md first. This is a proposed conditional classical
falsifier for the existing weak-isogeny source, not a new quantum candidate.
The target's real model-field Frobenius can complete the transported order
using powers 0,1,2 on both sides, with Rosati adjoints on the right. A
squarefree individually self-reciprocal factor test certifies success for
every hidden Lagrangian. Full-order certification still uses the integral
Gram determinant, not modular rank alone.

completion.py implements the spectral gate, public auxiliary-matrix
characteristic-polynomial acquisition, 144 weak completion actions, exact
reference-order completion and finite geometric/local consistency controls.
It does NOT implement curve-point torsion acquisition, geometric Gram/lattice
extraction or end-to-end recovery of a secret from a supplied weak isogeny.
replay.py regenerates receipt.json. test_completion.py contains regressions.

## Integration After The Checkout Is Safe

The intended Developer checkout was absent during this pass. Do not copy
into a moving staging tree or treat this isolated directory as the main
repository. No main CLI, UI, registry or Git files were changed.

For Gemini/Antigravity, once the verified checkout exists:

1. Map this result to the existing weak-isogeny candidate and classical
   attack records. Preserve status PROPOSED_CONDITIONAL_REVIEW_PENDING,
   supplied_weak_isogeny_constructed=false and geometric extraction=false.
2. Add a baseline through existing dequantization/run/proof commands only.
   Do not create another generic workbench or restore circuit search.
3. Keep the explicit common weak mask, full source order, genuine model
   field, fresh auxiliary levels, and field/point costs in the input schema.
   Do not silently give the attacker a descent, target order or ell points.
4. Adapt the public auxiliary-action interface to actual points. In the
   image basis, compute Frobenius coordinates by the existing pairings and
   small-r discrete logs. Charge those operations and extension fields.
5. Recover chi with M>12q0; factor at the ORIGINAL ell. UNKNOWN does not
   imply that the actual instance is hard. Do not select a replacement ell.
6. Build all 144 maps and their exact Gram using the written norm bound.
   Retain integer generator combinations during lattice reduction, verify
   determinant p^8, then call the existing kernel transport attack.
7. Add end-to-end tests ONLY when genuine geometric weak inputs exist. A
   reference-coordinate HNF or the p=5 curve alone does not meet that bar.
8. Run all repository tests, syntax checks, node --check index.js and
   qsearch.py validate after integration. These were not run on the migrating
   repository here. Preserve the negative controls and frozen dependencies.

## What Requires Further Reasoning

- Independent review of the local-to-global argument and complete input/cost
  composition. The earlier Rees-review authorization was already consumed;
  this bundle does not claim another independent review.
- Find a genuine growing-parameter weak-source subfamily meeting the public
  criterion, or prove an obstruction. The current curve has no constructed
  incoming source isogeny. No distributional coverage claim is justified.
- Investigate public target endomorphisms when the actual model-field
  Frobenius is scalar or the spectrum fails the sufficient criterion.
  Source words alone are already ruled out; hidden descents are not free.
- Pham 2609.17330v1 gives a conjugate-isogeny existence bound, not public
  acquisition from this weak interface. Its xi^2 scalar also prevents any
  gain from extra powers after failed one-step mixing; see Section 9.
- Reassess the quantum source's useful surviving domain after these tests.
  A route to cheaply sampling attractive inputs also needs a baseline for
  generating/solving the SAME input, not an unrelated hard oracle.

Do not spend the next reasoning pass on more local controls or CLI polish.
The unresolved work is geometric acquisition, scope, and surviving quantum
mechanism. There is no background search or autonomous worker in this bundle.
