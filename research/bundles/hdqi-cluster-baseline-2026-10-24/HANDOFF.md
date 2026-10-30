# Handoff: Uniform-Degree Classical Comparator

## Completed Scientific Work

Read CLUSTER_BASELINE.md first. It corrects the fixed-degree scope of the
published enumeration algorithm, then gives a local, unreviewed randomized
adaptation with an explicit uniform-degree small-temperature condition.
The finite reference checks embedding probabilities, contact multiplicities,
cluster factorials, signs, precision tails and the independent ordered-tuple
definition. It is not a scalable FPRAS or a quantum preparation result.

## Bounded Gemini Implementation Tasks

Only after the proof is reviewed and the repository migration is resolved:

1. Implement on-demand normalized polymer activity evaluation with certified
   absolute precision, following Section 6. Never replace a failed evaluation
   with zero or clip a value without preserving its error budget.
2. Reuse the explicit tree draw, but remove exhaustive reference catalogs.
   Add per-draw bit/operation accounting and aggregate Hoeffding, truncation,
   arithmetic and activity-approximation budgets separately.
3. Add CLI/registry access for the CLASSICAL comparator, retaining the exact
   rational admission condition D*(beta*Jmax)^2<=1/64. Outside that region
   return INCONCLUSIVE, not hard, quantum advantage, or a negative gap.
4. Expose the Section 7 field-generating-function extension separately:
   fields in [-1,1] cover pilot parity and zero-pin probabilities. Keep
   these distinct from physical thermal observables, full pilot samples
   and coherent pilot preparation. Mixed positive pins can cancel exactly;
   do not claim a sequential sampler from the avoidance estimator alone.
5. Test repeated polymers, signed weights, zero beta, tiny rational beta,
   high degree, unsuccessful embeddings, and exact failure probabilities.
   Production draws must not condition on acceptance unless the proposal
   normalization is explicitly included.

These are wiring tasks, not permission to promote the unreviewed theorem.
The research priority remains the weighted thermal gap or a decisive
counterexample, and a useful physical output after any preparation theorem.

## Workspace Safety

The intended Developer checkout is absent. Migration status remains
`needs_inspection`; original cloud files are retained. This bundle and the
external checkpoint are the complete change scope. Do not edit Desktop,
staging, Git, central registries, CLI or UI until the usable checkout is
verified. Prior bundles remain frozen so their receipt hashes remain valid.
No new reviewer or external outreach was started.
