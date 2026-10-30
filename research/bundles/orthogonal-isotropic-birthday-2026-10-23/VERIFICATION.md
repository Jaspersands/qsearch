# Verification

2026-10-23, isolated local bundle. No moving checkout edits.

- 23 new tests, including one deliberately failed/incomplete recovery that
  retains all actual query costs.
- The complete six-bundle selected milestone has 297 passing tests.
- Three Python source files pass py_compile.
- A second full replay reproduces the entire receipt byte-for-byte,
  including query histories and six source hashes.
- Five live recoveries at (n,p)=(3,3),(3,5),(4,3),(5,3),(4,13) all recover
  the exact supplied fixture subspace with the public exact certificate.
  Actual original-oracle calls: 67,53,85,297,358, respectively.
- The controller never receives the hidden L; it is private to the opaque
  fixture oracle. Supplied-secret kernel helpers occur only in tests.
- The uniform sampler's recursive incidence weights are exhaustively checked
  at rank two over F3, rather than inferred from a random histogram.
- Known public-frame arithmetic is checked at a 127-bit prime. That is not
  a large-field hidden-subspace recovery execution.
- No dense table is constructed. Safety limits reject accidentally
  exponential-sized classical runs before querying.

The receipt records every finite run, per-round cost and progress, three
unexecuted analytical schedules, and six source hashes. Finite successes
validate the controller and algebra, not the universal asymptotic proof.
No quantum execution, independent proof certification, novelty finding,
natural-source hardness, registry promotion or full-repository validation.
