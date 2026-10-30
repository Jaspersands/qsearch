# Verification

2026-10-25. All commands used /opt/anaconda3/bin/python, with warnings as
errors. Tests ran in separate fresh processes in their own bundle
directories to avoid collisions among historical standalone module names.

| Test file(s) | Passed | Pytest elapsed |
|---|---:|---:|
| test_regular_kernel.py | 29 | 4.00s |
| source-pullback-2026-10-23/test_pullback.py | 30 | 5.99s |
| source-residual-algebra-2026-10-24/test_residual_algebra.py | 29 | 21.37s |
| frobenius-order-completion-2026-10-25/test_completion.py | 25 | 1.97s |
| kernel-output-2026-10-23/test_kernel_output.py and test_uniform_source_bound.py | 47 | 6.74s |

160 tests passed, no skips or failures. Every invocation used:

```sh
/opt/anaconda3/bin/python -B -W error -m pytest -q -x -p no:cacheprovider TEST_FILES
```

The four new Python files passed py_compile. Two fresh standalone replay
processes produced byte-identical receipt.json files. All six source
hashes and 23 dependency hashes match. The replay additionally checks
five frozen completion sources, five completion dependencies, twelve
residual sources/dependencies and six product-corner source hashes.

Receipt SHA256:

```text
ffcae98ade2f3edf1dfa881621055b97f049d138b0214571aa7c98201f459ff7
```

Three integral arithmetic controls recover exact source pullbacks from
weak residue callbacks, acquire the characteristic polynomial from
auxiliary actions, return 4/2/1 candidates and select the reference
kernel using 9/5/0 calls to a finite opaque-label control. All seven
listed planes pass independent quaternion Hom-module integrality.
The unchanged ell=47 and ell=2^127-1 local controls return two candidates
each, with five interface calls each. Repeated spectra, including the
common-field product-Frobenius case, are not promoted.

These are exact arithmetic and interface tests, NOT proofs of the
general mathematical statements, independent review, a native geometric
source implementation, a native isogeny recovery or a quantum speedup.

Eight files were added in this external bundle plus an entry in the
external checkpoint. No main/staging files, registry, CLI/UI, Git,
migration state, previous proof or reviewer output was changed. The
intended Developer checkout was rechecked and remains absent. Full main
tests, node --check index.js and qsearch validate were not run against
the migration-sensitive source. No owned test/replay process remains.
