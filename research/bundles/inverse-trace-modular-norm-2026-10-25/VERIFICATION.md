# Verification: 2026-10-25

Completed against the isolated local research bundles, not the Desktop repo.

- 38 new tests PASS, including full native round-trip, non-square P,
  factor-cap UNKNOWN, scoped public-carry negatives, independent native
  verification, extension embedding/descent, all three scalar-kernel ranks,
  exhaustive 33-unit conic controls over F_32, complementary lifts, and exact
  counting bounds. No skips; Python warnings treated as errors.
- Combined new + predecessor norm-transfer + residual-SAT suites:
  88 tests PASS in 1.33 seconds. This includes 50 existing tests.
- Three Python sources compile successfully without bytecode writes.
- Live receipt generated; a fresh second run matches it exactly and checks
  all ten source/dependency hashes. Predecessor receipt and four predecessor
  source hashes are unchanged.

Commands, from this directory with /opt/anaconda3/bin/python:

    python -B -W error -m pytest -q -p no:cacheprovider test_modular_norm.py ../inverse-trace-norm-transfer-2026-10-23/test_norm_transfer.py ../inverse-trace-residual-2026-10-23/test_residual_sat.py
    python -B verify_modular_norm.py --write
    python -B verify_modular_norm.py --check

Receipt SHA256:

    ca9170b9b06fc50c7454080837841cfb6681e71b6cc0430df889c654186c9fab

Frozen native input: n=7, binary modulus 131, N=49, K=6, original supplied
points and all-one targets. The known witness was replayed from the earlier
receipt, not newly planted or found by this pass's new method. Its earlier
baseline cost was 44 trials and 3694 field draws. The initial diagnostic
reran that bounded predecessor baseline; receipt generation uses frozen
evidence and runs no new seed search.

Known-witness control: degrees (P,Q,A,W)=(42,48,48,47); P has 21 nonzero odd
coefficients. Given its EXTRA W, the solver has 32 factor orientations,
checks 14, tries one normalized unit, and returns an independently verified
native witness. Kernel-rank counts are [0,1,13]. This is not public carry
acquisition. A cap of one returns UNKNOWN without checking orientations.

Public controls: W=0 excludes its sole orientation; W=X excludes four
orientations, all by rank two; W=1 has odd norm degree; W=X^3+X has an inert
factor of odd multiplicity. These exclude only the specified carries. The
same native input remains satisfiable by the frozen witness.

The uniform-carry bound at n=17 and n=31 is exact symbolic counting, not
an executed large-field search. The written proofs have not received a new
independent review or Lean formalization. The previously authorized Rees
reviewer was not reused for this work.

Changes: seven new bundle files, including this record and receipt, plus
the external research checkpoint. No edits to main/staging checkout,
CLI/UI, registry, Git, migration, prior proofs, or prior receipts. The
intended Developer checkout remains absent at the final path check.
Full-repository tests, qsearch.py validate, and JavaScript checks were not
run against the moving source. No quantum execution or advantage claim.
