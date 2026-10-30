# Verification: Odd Scalar Content

2026-10-25, isolated local research workspace. No main/staging/dependency
edits, main CLI integration, commit or push. All source/recovery claims
remain conditional and independently unreviewed.

## Commands

From `/Users/jaspersands/Developer/qsearch-research-work`:

```sh
env OPENBLAS_NUM_THREADS=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /opt/anaconda3/bin/python -m pytest -q -p no:cacheprovider -W error odd-content-reduction-2026-10-25 cyclic-odd-degree-source-2026-10-25 prime-only-source-2026-10-25 kernel-output-2026-10-23/test_uniform_source_bound.py kernel-output-2026-10-23/test_kernel_output.py smooth-repolarization-2026-10-23/test_smooth_repolarization.py prime-square-flags-2026-10-23/test_prime_square_flags.py
```

232 PASS in46.87s, warnings-as-errors, no skips. Includes24 new content
tests. The preceding23-test run before the supplied degree225 control also
passed; no failed tests or repairs in this pass.

```sh
/opt/anaconda3/bin/python -m py_compile odd-content-reduction-2026-10-25/content_reduction.py odd-content-reduction-2026-10-25/controls_content.py odd-content-reduction-2026-10-25/replay_content.py odd-content-reduction-2026-10-25/test_content_reduction.py
env OPENBLAS_NUM_THREADS=1 /opt/anaconda3/bin/python odd-content-reduction-2026-10-25/replay_content.py --write --check
env OPENBLAS_NUM_THREADS=1 /opt/anaconda3/bin/python odd-content-reduction-2026-10-25/replay_content.py --check
```

All PASS. Four syntax checks and two separate replay executions succeeded.
Receipt SHA256:
`694491bbc3433116c00081fcb41eed65f2b6e5e8efdfcc5f8cd38aa0308d2123`.

## Evidence And Limits

- Supplied Smith-subgroup cases recover contents3,75,15 and residual
  degrees27,27,1 respectively, including mixed and entirely scalar kernels.
- The tests check both probe axes, full-modulus symplectic/CRT legality,
  monotone/parity rejection, smaller-modulus affine lifts, exact full-source
  certificates for nonfree kernels, and original ideal index/annihilation.
- For supplied phi=3(3+4i) in characteristic11, degree225 and content3,
  the computed original ideal equals O*phi in both lattice directions.
- The protocol uses no secret kernel to form its public query schedule.
  The finite membership controls do use supplied kernels and are labelled
  accordingly. No native marked labels, unknown directions or geometric
  quotients are computed. No quantum execution or speedup is established.
- Main repository tests, `qsearch.py validate` and Node/UI checks were not
  run: this is an isolated theory pass while the main checkout remains
  unverified. The prior one-reviewer authorization was not reused.

The full2025 Chen--Petit PDF still could not be retrieved. Its public
abstract confirms prior general-degree coverage; it does not substitute
for a complete proof/assumption comparison. That gap is documented rather
than inferred away. Goal remains ACTIVE.
