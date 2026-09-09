# Proof-Route Provenance

`python qsearch.py proof-routes` audits the pinned contracts in
`research/registry/proof_routes.json`. `python qsearch.py proofs` includes
the audit, and `python qsearch.py validate` rejects unsupported asserted
levels. Initial setup is `proof-routes --initialize`; it refuses to overwrite
an existing manifest. Routine audit runs never refresh evidence hashes.

## Meaning

This is a **dependency and provenance checker, not a mathematical prover**.
A scoped attestation in a source file is still a research assertion. The
checker does not establish that the source proves its recorded conclusion.
`derived-review-pending` deliberately preserves that distinction. It does
not accept a `machine-checked` label without an implemented checker backend.

Claims identify the domain, input model, quantifier and conclusion explicitly.
Each proof route needs its own scoped conclusion attestation. Premises alone
cannot supply another conclusion, so encoded carrier access does not
automatically become a decoder or turn an identification bound into a binary
decision bound. Scope equality is literal; any generalization or restriction
needs an explicitly reviewed bridge attestation.

Routes are alternatives (OR). Within a route, premises, conclusion evidence
and diagnostic checks are required together (AND). A least-fixed-point
evaluation prevents circular self-certification while allowing independently
grounded alternatives to support downstream claims. Claim ordering cannot
change support. Failing one route does not invalidate another.

The conservative evidence levels distinguish observations, exact finite
results, and review-pending uniform derivations. Finite support cannot be
automatically promoted into a universal conclusion. This initial system is
not a general induction calculus: record an explicit reviewed uniform bridge
and keep its base-case computations as diagnostics, rather than inferring
uniformity from an experiment table.

## Provenance and Diagnostics

Evidence pins the SHA256 of its file. Missing files and changed hashes make
the corresponding route unavailable. Diagnostic predicates use JSON pointers
and type-sensitive equality: integer 1 is not boolean true. A failed predicate
is a failed diagnostic, not automatically a mathematical counterexample.

If rerunning an experiment changes a pinned artifact, including its timestamp,
the pin becomes stale. Review the changed artifact and source before updating
the manifest. Do not regenerate hashes merely to restore a green validation.
Versioned immutable artifacts or explicitly defined semantic hashes can be
added later; the current whole-file policy is intentionally transparent.

## Initial Coverage

Thirteen curated contracts cover the systematic local-proof gap, independent
global suffix/surface argument, conditional encoded restriction, and the
fixed-reference identification bound, plus reference-orbit block purity and
separately scoped predetermined/adaptive discard-information bounds.
The adaptive route uses the conditional orbit purity, not an invalid transfer
from an averaged mixture bound to a posterior-conditioned bound.
Four claims remain unresolved: uniform
cubic local loss, the local systematic argument, impossibility of efficient
binary detection, and existence of a hidden-involution decoder. Unresolved
binary impossibility means no no-go is established, not that a decoder exists.

The global BABA argument remains supported at review-pending level independently
of the missing local route. The encoded construction remains conditional on
compatible QFT primitives and a known reference subgroup. No speedup or formal
proof is certified. Most of the repository is not yet covered by this manifest.

## Next Work

Expand through high-impact live claims before bulk migration. Add explicit
counterexample witness replay, immutable artifact versions, carefully scoped
reduction bridges, and a real formal-checker integration. Any automated
literature or hypothesis system should propose attestations for review, not
silently raise their evidence levels.
