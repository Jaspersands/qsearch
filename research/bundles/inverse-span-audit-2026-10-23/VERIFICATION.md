# Verification

2026-10-23. Isolated local research work; no moving checkout edits.

- **13 tests passed in 0.27s** using `/opt/anaconda3/bin/python`.
- Both Python files passed `py_compile` after the final test edit.
- The live receipt enumerated **11,811** binary subspaces in each of
  dimensions three and four over F128, with no duplicate RREF subspaces.
- A separate FLINT polynomial implementation checked every inverse and
  trace in the counterexample. All 128 binary combinations of its seven
  independent inverse values give all 128 field elements.
- All 127 nonzero scalar rescalings fail the trace-zero predicate.
- The regenerated receipt's four source hashes match the actual files.

Pytest plugin autoload and its cache provider were disabled. Bytecode was
redirected to `/tmp/qsearch-inverse-span-pycache`. No external solver was
invoked: the existing residual module was imported only for its tested
binary-field arithmetic, not for its Z3 search routine.

The receipt is an exact algebraic counterexample, NOT a native codeword
experiment, an asymptotic classical lower bound, a normality theorem for
growing fields, or a quantum execution. The new literature's full main
theorem has not been independently proved here. The complete repository,
CLI, UI and registry were not tested or modified during migration.
