# Verification

- Initial bound suite: 24 passed in 0.59s. Final suite including the
  one-sided action control: 27 passed in 0.93s.
- Five Python files pass py_compile with bytecode outside the checkout.
- replay_native_input.py completed for five prime multipliers, up to
  2^127-1. Its conservative single-trial exponents are -29, -62, -152,
  -431 and -924, for the stated independent-mark experiment only.
- The padded-source control checks all 51,840 group elements against all
  24 gluings: a common subgroup of size 54 and zero disagreements. The
  general no-go is the subspace argument, not an extrapolation from this.
- Receipts include source fingerprints; verification is repeated after the
  final replay to detect stale artifacts.
- No geometric global-consistency test, source acquisition, coherent
  oracle, or general quantum speedup was executed or established.
- Full-repository validation, CLI/UI integration, commits and pushes were
  not performed while migration is active.
