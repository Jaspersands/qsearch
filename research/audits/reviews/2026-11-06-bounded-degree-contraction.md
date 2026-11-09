# Bounded-degree contraction review ledger

2026-11-06. Exact scope: research/BOUNDED_DEGREE_CONTRACTION_BASELINE.md.
This is a source-based written composition, not a full ETH manuscript audit.

- Codex independent_direction_selection reviewed actual source lemmas
  swaps-matrix/support/forms, incidence labels/embedding, coefficients, layout
  and parameter choice. No blocker found. Parent read and checked the actual
  source, especially the r factor, repeated variables and integer row norms.
- Claude Opus/high independently reviewed prop:general-count from the saved
  source excerpt. No algebraic blocker found. Total degree and rational
  kernels are explicit source conventions. Its remaining bit-cost obligations
  are met by this note's FIXED K and explicit constant-arity contract, not by
  an arbitrary abstract algebra. No full-paper endorsement was requested or
  inferred. Run: ../claude_runs/2026-11-06-counting-identity-opus/; completed
  end_turn, 10500 input/14246 output tokens, estimated USD0.32692. The finite
  example suggested by Claude was independently superseded by the parent's
  four-variable nontrivial-kernel exact control; no asymptotic inference.
- Final actual-text source/scope review by independent_direction_selection
  accepted Steps1-6 and circuit parameter transfer, requiring L>=n so unused
  variables cannot create an uncharged output. Parent repaired the contract
  to require an explicit variable list, with original count charged.
- Final actual-text bit/circuit review by superlattice_source_scope accepted
  after that repair and the explicit incidence-sum degree upper bound.
  Denominators B*a^d, partial-group products, sum sizes, fixed-field norms,
  Hermite inverse heights, polynomial space and n<=2G all checked. Time
  comparisons use the minimum applicable baseline; space bounds stay distinct.
- One alleged duplicated subset sum in the primary source was REJECTED after
  parent inspection. The reviewer confirmed its cause was overlapping sed
  ranges printing the same line twice. No source defect is recorded.
- Scope retained: no sharper quantitative appendix, full ETH theorem, novelty,
  polynomial simulation, approximate sampling, adaptive/succinct/oracle gate
  model, arbitrary real entries or quantum exact-amplitude algorithm claim.

Exact control: ../controls/boolean_product_interpolation/exact_control.py
and JSON. Four variables, K=Q(zeta8), Q3,R2,J3; nine jets/full Hermite polynomial
match direct sum. H0=18+7*zeta-zeta^2. Wrong x-dependent corrections and missing
fixed-bit restrictions are rejected. This is a supplied-design control only.
