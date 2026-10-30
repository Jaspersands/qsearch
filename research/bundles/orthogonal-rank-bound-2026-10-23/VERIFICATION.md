# Verification

2026-10-23. Local isolated bundle only; the Desktop checkout is migrating.

- 43 new tests passed in 3.35 seconds.
- Combined run with orthogonal-three-probe, central-rank,
  quadratic-cancellation and scalar-cancellation: 274 tests passed in
  5.34 seconds. This is NOT the full repository suite.
- rank_bound.py, test_rank_bound.py and replay.py pass py_compile.
- Live replay writes rank_bound_receipt.json with three complete finite
  orbit controls, seven analytical scaling deductions and six source hashes.
- A full deterministic receipt replay matched; the receipt was regenerated
  after adding the subsequent stronger-classical-baseline cross-reference.
- The primary PDF's Section 3.2 definitions, parameter table, and Lemma 3.14
  statement were checked in rendered pages as well as extracted text.

No scalable quantum circuit, natural source, cryptanalytic application,
formal proof or novelty certification was executed. No repository CLI,
registry, JavaScript, Git or UI state was changed. Full repository validation
is intentionally deferred until migration finishes.
