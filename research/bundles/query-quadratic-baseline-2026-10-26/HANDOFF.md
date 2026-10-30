# Handoff: Query-Quadratic Classical Admission Gate

Read QUADRATIC_BASELINE.md. This is a known classical method applied and
costed on the actual full-suborder query input, not a new quantum candidate.
The paper's standard primitivisation result is attributed there. The new
index-only specialization and exact baseline counts are parent deductions,
not independently reviewed or executed on native curves.

## Scientific Changes

1. Being outside the integral coset H is no longer an adequate criterion
   for unexplained geometric progress. Scalar-centered division by d
   already succeeds on d(d-1) of the d^4 source queries.
2. Start a query's quadratic gate from S0=R intersect Q(beta), not Z[beta].
   Since Smax/S0 injects into O/R, only supplied index primes are needed.
   Test the unique odd-prime quadratic overorder using ACTUAL native division.
3. If this gate produces a new map, record a classical success and restart
   with the enlarged normalized order. If it does not, a useful geometric
   corner for nonscalar beta must be outside R AND noncommuting with beta.
4. In the native q-neighbor non-Bass family, the same uniform queries have
   prime-division growth probability (q^2-1)/q^3. Do not compare geometry
   only against the much weaker approximately q^-9 full-index division.
5. The gate's no-growth filter is not proved constant on hidden cosets.
   The prior conditional 1/3 theorem cannot be reused after this filtering.
   Keep raw sample denominators and UNKNOWN outcomes, not renormalized hits.

## Mechanical Work For Gemini, When Safe

The helper quadratic_gate.py is intentionally small and native-free. It
constructs primitive intersection generators, validates a SUPPLIED index
factorization and proposes scalar/prime divisions. Its proposals explicitly
have native_integrality_certified=false. The tests use supplied orders only
to check them; do not expose that fixture as a native backend.

After the main checkout is available and safe, integrate these arithmetic
checks into the existing baseline stage, not a new framework. Normalize
the R basis to start with1 before using the gcd intersection shortcut.
Keep native division, returned map handles, trace-coordinate growth tests,
normalization and compact evaluator costs explicit. A missing backend must
produce UNKNOWN, never a claimed rejection or successful saturation.

Useful result fields for ACTUAL native experiments are the original query
count, scalar status, quadratic baseline outcome, native certificate IDs,
old/new index, remaining geometric growth and whether that new corner
commutes with beta. Do not fabricate records from these supplied-coordinate
controls or create a toy oracle benchmark to fill those fields.

No new CLI, UI, registry or dashboard is needed for the current isolated
mathematical pass. The moving original checkout and all prior source/review
receipts were left unchanged. No commit or push was made.

## Next Research Decision

The specific missing mechanism is a useful TRANSVERSE native symmetry on
the large-prime non-Bass input after this complete query-quadratic gate,
not merely a nonintegral beta or a large automorphism group. Seek a
constructive family or a broad source-specific obstruction before spending
more on nearby finite controls. An automorphism-count sweep or another
known-order positive example does not answer the question.

If this cannot yield a credible constructive route, freeze the harvest
subdirection as an unresolved comparator and revisit independent source
mechanisms. Do not let maintenance of classical filters become the entire
research program. The reviewed additive reduction itself remains a possible
restricted assumption-removal result with novelty still unestablished.
