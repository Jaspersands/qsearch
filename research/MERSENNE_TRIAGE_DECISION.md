# Mersenne Research Triage

30 October 2026. Six focused agents plus parent integration. This pass
produced a concrete classical search attack and scoped mathematical audits,
not a new quantum algorithm. No commits, pushes, installs or outreach.

## Decision

Retain the explicit family and its valid mathematics, but shelve it as a
priority route to a major NEW quantum algorithm. Its quantum receiver uses
published decoding/Fourier machinery. No significant external problem has
been reduced to this family, and its formerly unresolved small native
search fixtures now have direct classical witnesses. Failure of other
classical methods does not establish hardness or rescue the significance
claim. Do not change exponent or input distribution to evade an attack.

Reopening requires a concrete new algorithmic mechanism, a useful nonlocal
reduction with a paid source, or a general native classical solver/sampler.
Larger instances, more negative controls, receiver wiring and a shorter
conditional-count bound alone are not reopening criteria.

## Concrete Outcome

The parent derived and Aristotle implemented the [scalar-flat attack](MERSENNE_SCALAR_FLAT_ATTACK.md).
Lovelace independently reviewed the local proof; Raman checked it separately.
Parent replayed all three fixed inputs and their independent integer-field
verifiers. Original points, target bits, field representation and all parity
rows are preserved. There was no seed search, planted witness or global
restart. Each coordinate succeeded at its first translation.

| Input | Rank | Verification |
|---|---|---|
|n17, s3, all-one targets, seed17030|612/612|native witness valid|
|n17, s3, popcount targets, seed17031|612/612|native witness valid|
|n31, s7, all-one targets, seed31030|3720/3720|native witness valid|

The method constructs direct accepted x-flats, then solves binary linear
equations inside their product. It does not assume those flats have affine
lifts. The local probability guarantee is proved, with a finite random-bit
clock; a global success theorem is not. The guaranteed local dimension is
logarithmic in n, insufficient for automatic full row rank asymptotically.
The outputs are witnesses, not certified uniform samples.

## Agent Conclusions

1. **Feynman: conditional estimation.** A positive-Fourier minorant proves
   exponential variance for the best unbiased single-dual-character importance
   estimator in an explicit residual window, even granting its optimal
   proposal for free. Raman independently checked Sections2-4 and the exact
   arithmetic. This is NOT a general counting/sampling lower bound: nearly
   flat counts make the constant estimate1 good on most syndromes. A separate
   smoothed-count construction remains a written, not independently reviewed,
   extension. [Audit](audits/reviews/2026-10-30-mersenne-conditional-estimator.md).
2. **Lovelace: algebraic solving.** The quartic parametrization satisfies a
   Chevalley-Warning degree inequality, but parity of counts is not a solver.
   A native h=0 homogenization counterexample invalidates a proposed output
   contract. Binary diagonal equations would be easy; simultaneous handling
   of the mixed quartic and local predicates is the missing reduction.
   [Audit](audits/reviews/2026-10-30-mersenne-underdetermined-solver.md).
3. **Noether: block resampling.** A fixed-buffer heat bath has a polynomial
   ideal spectral-gap bound. Its specified exact conditional update still
   costs about2^K trials. The older overlapping-block coupling is credited,
   not repackaged as new. A scalar-flat witness cannot replace a uniform
   conditional draw. [Audit](audits/reviews/2026-10-30-mersenne-block-resampling.md).
4. **Dirac: final Fourier conditioning.** Local pair overlaps contract to
   small counter polynomials, but one signed global codeword sum remains.
   Punctured complete lists eventually have explicitly exponential size;
   dephasing loses almost all parity-valid probability. These are scoped
   identities/falsifiers, not native hardness. [Audit](audits/reviews/2026-10-30-mersenne-fourier-list-contraction.md).
5. **Raman: research value and adversarial review.** The generic prime-power
   quantum framework applies after the family-specific source/tail premises
   are paid. Prime-field OPI and oracle-hardness claims do not transfer
   automatically. No credible distinct breakthrough deliverable emerged;
   shelving as a priority is an allocation decision, not an impossibility
   result. [Audit](audits/reviews/2026-10-30-mersenne-research-value.md).
6. **Aristotle: executable attack.** Implemented strict tagged inputs,
   original-parity restriction, finite bit accounting, an independent verifier,
   fixed-case reports and regression tests. Parent rejected an initial hidden
   `randrange` rejection clock; the final code requests a bounded number of
   bits and reruns the SAME input seeds after that correction.

## Handoff Boundaries

Do not describe these outcomes as a Shor-level result, an asymptotic
dequantization, or uniform native sampling. Do not reopen already closed
local Fourier access as an assumed oracle. Keep theory, finite arithmetic,
live native classical witnesses and actual quantum execution distinct.

There is no urgent receiver/UI task for the separate implementation agent.
The next research pass should compare remaining concrete, unsolved routes
against their CURRENT classical filters, and select a useful source or
standalone algorithmic theorem before requesting more infrastructure.
Detailed verification and replay status are recorded in `AGENT_HANDOFF.md`.
