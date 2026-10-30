# Independent Review Resolved

The independent review is ../systematic-review-2026-10-27/REVIEW.md.
It accepts the exact all-syndrome character identity, systematic and affine
probabilities, capped conditional-uniform output law, and tower tail bound.
Its128 independent inclusion-exclusion/character comparisons and285 capped
output identities passed, with100 unsigned-weight and116 omitted-phase
mutations detected. Parent tests separately exercise the actual implementation.

Corrections incorporated in BASELINE.md:

- Compare only to the WORST-RANK specialization of the displayed four-list
  upper bound, on its certified tower range e>=64. Actual rank is unknown.
- The rate threshold assumes polynomial other costs and a limiting r_2/e;
  it is not a necessary condition on all future four-list implementations.
- Retain the existing polynomial norm solver for the special near-canonical
  cofinal subclass. The unresolved family allows arbitrary admissible classes.
- The sampler's two-sided asymptotic expected cost is exponential in e,
  subexponential in dense input bit length, not a classical lower bound.

The reviewer also points to Nagy-Pach's general AJT-type existence theorem:
two disjoint column bases and p=100003 suffice for native all-syndrome
existence, but a polynomial witness-extraction algorithm was NOT established.
This is a follow-up classical falsifier, not a new hardness assumption.

The implementation now caches the particular solution once per sampled
syndrome. The reviewer inspected that final code. No ideal-coin law is
claimed for deterministic seeded replay. No quantum speedup follows.
