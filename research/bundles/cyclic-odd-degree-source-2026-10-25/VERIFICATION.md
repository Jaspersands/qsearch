# Verification: Odd Cyclic Source Extension

2026-10-25. Isolated workspace:
`/Users/jaspersands/Developer/qsearch-research-work`.
The intended local main checkout was checked again and is still absent.
No moving-source, staging, Git, CLI, UI or main registry edits were made.

## Final Commands And Results

Python: `/opt/anaconda3/bin/python`.

```sh
env OPENBLAS_NUM_THREADS=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /opt/anaconda3/bin/python -m pytest -q -p no:cacheprovider -W error cyclic-odd-degree-source-2026-10-25
```

37 PASS in4.29s, no skips.

```sh
env OPENBLAS_NUM_THREADS=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /opt/anaconda3/bin/python -m pytest -q -p no:cacheprovider -W error cyclic-odd-degree-source-2026-10-25 prime-only-source-2026-10-25 kernel-output-2026-10-23/test_uniform_source_bound.py kernel-output-2026-10-23/test_kernel_output.py smooth-repolarization-2026-10-23/test_smooth_repolarization.py prime-square-flags-2026-10-23/test_prime_square_flags.py
```

208 PASS in45.20s, warnings-as-errors, no skips. This is a scoped regression
of the source chain, NOT the entire Desktop repository's test suite.

```sh
/opt/anaconda3/bin/python -m py_compile cyclic-odd-degree-source-2026-10-25/cyclic_source.py cyclic-odd-degree-source-2026-10-25/controls_cyclic.py cyclic-odd-degree-source-2026-10-25/replay_cyclic.py cyclic-odd-degree-source-2026-10-25/test_cyclic_source.py
env OPENBLAS_NUM_THREADS=1 /opt/anaconda3/bin/python cyclic-odd-degree-source-2026-10-25/replay_cyclic.py --write --check
env OPENBLAS_NUM_THREADS=1 /opt/anaconda3/bin/python cyclic-odd-degree-source-2026-10-25/replay_cyclic.py --check
```

All PASS. Four files syntax checked. The independent second replay matched.
Receipt SHA256:
`19a75cc0826394ec4d6353243a6164848e008813586a66d5b128daacfd744def`.
The receipt hashes this bundle's implementation, tests, proof and handoff,
the used source dependencies, and the retained PPAV paper.

## Observed Failures And Repairs

- Initial modular symplectic assertions compared residues against an
  unreduced form containing -1. Fixed to subtract the form before reduction.
- The new degree25 check initially passed a residue matrix to an evaluator
  requiring an exact integer quadratic identity. It now checks the identity
  modulo the actual torsion prime, then evaluates u+vH blockwise modulo
  that prime. The exact-integer evaluator and all old dependencies remain
  unchanged. Final reruns above include the repaired test.
- The mod9 equal-stabilizer counterexample is a genuine mathematical
  obstruction to the naive one-factor certificate, not an implementation
  bug. The new cross-factor certificate is tested against it.

## Receipt Scope

For n45 and characteristic11 the public uniform plan has460 quotient
primes, maximum weak order3313, a2304-bit trace bound and4618-bit multiplier.
Geometric dimension16 and r^16 point-list costs remain. Zero kernel points
were enumerated. The 456 coherent/913 classical source-query budget is an
IDEAL analytical sampling bound at error2^-40, not an executed receiver.
Source-clock and approximate-preparation/QFT error are additional.

The alpha=3+4i degree25 control checks actual order identities and local
Tate actions, including cyclicity and nonsemisimple prime3. The map and
postprocessing lines are supplied. No unknown kernel is recovered.

Main `qsearch.py validate`, main tests, and `node --check index.js` were not
run because the main checkout is not yet verified local and was not edited.
No native geometric backend, coherent circuit, advantage, novelty claim or
independent review was completed. Scope flags remain false. Goal ACTIVE.
