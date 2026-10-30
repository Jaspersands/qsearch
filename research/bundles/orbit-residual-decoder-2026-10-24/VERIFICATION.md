# Verification

2026-10-24. External bundle only; main checkout still unavailable for safe
integration. No main qsearch validate, repository-wide tests, Node/UI checks,
Git operations, migration changes, or additional subagent review occurred.

- 30 new controls plus 529 preceding external controls: **559 passed in
  6.24s**, warnings as errors, plugin autoload disabled, no skips.
- `py_compile` passed for orbit_decoder.py, test_orbit_decoder.py,
  make_receipt.py, with bytecode redirected outside the source checkout.
- Receipt replay byte-identical; all eight resident predecessor SHA256 values
  matched. Source hashes are embedded in the regenerated final receipt.
- Large basis-only control p2053,m3,n204,weight50,cap51: VERIFIED_UNIQUE,
  rank50, exact full label recovery from syndromes only. This is NOT a
  quantum state or a halfset-source sample, and produces no native P.
- Three exhaustive p19 controls each checked 130321 free assignments.
  Nonzero fixed last-frequency tuples (1,1) and (2,7): 342 failures,
  fraction18/6859, below20/6859. Invalid tuple(0,0):1045 failures,
  fraction55/6859, exceeding that valid-source bound as expected.
- Exact finite ideal bound: p12289,M4096,n9828,D2375,C2376;
  discarded mass <5.858e-25, perfect-search failure <3.135e-9.
  Full circuit error must be added; no physical or simulated quantum run.
- Tests also cover whole-cap competitors, a concrete score alias, invalid
  source coefficients, initial truncation normalization, root/field/input
  rejection, and split/anisotropic/higher-width classical flat controls.

The mathematical derivation remains LOCAL UNREVIEWED. These tests do not
prove novelty, classical hardness, a natural-problem reduction, or practical
quantum resource costs. All corresponding receipt admissions remain false.

Late audit correction: the existing cubic_orbit_decoder already implements
the source, general rank formula, guard, phase checks and classical portfolio.
The new scientific delta is the perfect-search/truncation bound, not those
earlier ingredients. Two additional predecessor hashes record that source.
