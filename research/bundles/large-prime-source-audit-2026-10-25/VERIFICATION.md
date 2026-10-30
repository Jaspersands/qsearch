# Verification

2026-10-25, isolated local research workspace only. Main checkout remains
absent at the intended Developer path. No moving source/staging edits,
CLI/UI integration, central registry change, commit or push. No additional
reviewer was used; the earlier authorized Rees review is a different proof.

Focused run: 20 PASS in 0.59s, warnings as errors, no skips. Combined source
milestone: 406 PASS in 58.29s, including the earlier 386-test scope and all
20 new controls. Command from `/Users/jaspersands/Developer/qsearch-research-work`:

```sh
env OPENBLAS_NUM_THREADS=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /opt/anaconda3/bin/python -m pytest -q -p no:cacheprovider -W error large-prime-source-audit-2026-10-25 elliptic-field-normalization-2026-10-25 source-field-audit-2026-10-23 native-membership-baseline-2026-10-25 double-level-source-2026-10-25 odd-content-reduction-2026-10-25 cyclic-odd-degree-source-2026-10-25 prime-only-source-2026-10-25 kernel-output-2026-10-23/test_uniform_source_bound.py kernel-output-2026-10-23/test_kernel_output.py smooth-repolarization-2026-10-23/test_smooth_repolarization.py prime-square-flags-2026-10-23/test_prime_square_flags.py
```

Four new Python files passed py_compile. `replay_calibration.py --write --check`
and a separate `--check` both passed. Receipt SHA256:
`84924b8a1c8552067cd321aa96e938fd67f7e1e38368e477bacd56284d49a524`.
No required process remains running. Main tests and qsearch.py validate were
not run because this isolated pass does not edit or integrate the main repo.

The general calibration argument is elementary linear algebra. Controls
enumerate 200 mask assignments and five supplied quaternion-map reductions;
they do not execute actual curve arithmetic, quotient geometry, a native
unknown-map problem or any quantum algorithm. Global evaluator consistency
remains an input promise. All receipt flags for such execution, independent
review, novelty and advantage are false.
