# Verification

2026-10-25. Isolated local research workspace; no moving source, staging,
main registry, CLI/UI or Git changes. No additional independent reviewer.

## Commands And Results

Final scoped source regression from `/Users/jaspersands/Developer/qsearch-research-work`:

```sh
env OPENBLAS_NUM_THREADS=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /opt/anaconda3/bin/python -m pytest -q -p no:cacheprovider -W error suborder-transcript-2026-10-25 large-prime-source-audit-2026-10-25 elliptic-field-normalization-2026-10-25 source-field-audit-2026-10-23 native-membership-baseline-2026-10-25 double-level-source-2026-10-25 odd-content-reduction-2026-10-25 cyclic-odd-degree-source-2026-10-25 prime-only-source-2026-10-25 kernel-output-2026-10-23/test_uniform_source_bound.py kernel-output-2026-10-23/test_kernel_output.py smooth-repolarization-2026-10-23/test_smooth_repolarization.py prime-square-flags-2026-10-23/test_prime_square_flags.py
```

451 PASS in 59.02s, warnings-as-errors, no skips. This includes 45 new
suborder tests, 20 projective-calibration tests and the earlier 386-test
source scope. It is not the entire main repository test suite.

```sh
/opt/anaconda3/bin/python -m py_compile suborder-transcript-2026-10-25/suborder_transcript.py suborder-transcript-2026-10-25/controls_suborder.py suborder-transcript-2026-10-25/test_suborder_transcript.py suborder-transcript-2026-10-25/replay_suborder.py
env OPENBLAS_NUM_THREADS=1 /opt/anaconda3/bin/python suborder-transcript-2026-10-25/replay_suborder.py --write --check
env OPENBLAS_NUM_THREADS=1 /opt/anaconda3/bin/python suborder-transcript-2026-10-25/replay_suborder.py --check
```

All four syntax checks and both receipt checks PASS. Receipt SHA256:
`1fbf7c2e49553c416131856849358f1552565f59e9251af87f3ee8fd2672a721`.

## Debugging Record

An initial unknown-depth control used a rational inverse for a frame only
known invertible modulo the torsion order. Eleven cases failed. Replaced it
with the existing modular inverse; all cases now pass. The first receipt
serialization also exposed SymPy integer entries; explicit integer conversion
fixed it, and a serialization/scope-gate regression test was added. Neither
failure was suppressed, skipped, or worked around by weakening assertions.

## Evidence And Limits

- Fifteen recorded supplied-map controls cover degrees 2,25,11,22, including
  a p-divisible nonprimitive suborder scale. Each transcript uses 8 known
  source and 8 known suborder calls, zero unknown-isogeny calls, and 2*r^2
  coordinate-table entries. Actual curve-point generation remains false.
- The scalar-multiple countercontrol gives identical projective transcripts
  and dictionaries at degrees 2 and 8. Only the primitive map is covered
  by the proposed degree-divisibility lemma.
- A degree-22 supplied map yields trace 13010 and an integral half-polarization
  at query modulus 2, with no split at p=11 and no characteristic padding.
- Unknown-depth tests cover primes 2,3,5, ambient exponents 1-4, every smaller
  depth and five primitive directions: 210 exact kernel controls, not native
  hidden-oracle experiments. A supplied degree-25/275 pair has equal right
  orders as rational lattices despite the inseparable factor.

The local conversion is implemented. The written global reduction is pending
independent review and full geometric composition. No effective target order
from unknown input, native geometric source, quantum execution, novelty or
speedup was established. Main qsearch.py validate and node checks were not
run because the main checkout is not integrated or edited. Required command
processes completed. Goal remains ACTIVE.
