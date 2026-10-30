# Verification: Classical Signed-Word Sampler

Date: 2026-10-24. Scope: external local research bundle only.

## Executed

The combined suite passed **226 tests**: 49 new sampler controls and 177
prior cluster, relative-flow, Rees class-three, parent-gap, filtered-parent
and mass-comparator controls. Warnings were errors; plugin autoload and
pytest cache were disabled. No test was skipped.

From `/Users/jaspersands/Developer/qsearch-research-work`:

```sh
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONPYCACHEPREFIX=/tmp/qsearch-sign-pycache PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /opt/anaconda3/bin/python -m pytest -q -p no:cacheprovider -W error hdqi-sign-sampler-2026-10-24/test_sign_sampler.py hdqi-cluster-baseline-2026-10-24/test_cluster_baseline.py hdqi-relative-flow-2026-10-24/test_relative_flow.py rees-class-three-2026-10-24/test_class_three.py hdqi-parent-gap-2026-10-23/test_parent_gap.py hdqi-filtered-parent-2026-10-24/test_filtered_parent.py hdqi-gap-baseline-2026-10-24/test_gap_baseline.py
env PYTHONPYCACHEPREFIX=/tmp/qsearch-sign-pycache /opt/anaconda3/bin/python -m py_compile hdqi-sign-sampler-2026-10-24/sign_sampler.py hdqi-sign-sampler-2026-10-24/test_sign_sampler.py
/opt/anaconda3/bin/python hdqi-sign-sampler-2026-10-24/sign_sampler.py
/opt/anaconda3/bin/python hdqi-sign-sampler-2026-10-24/sign_sampler.py --output /tmp/qsearch-sign-replay-2026-10-24.json
cmp hdqi-sign-sampler-2026-10-24/receipt.json /tmp/qsearch-sign-replay-2026-10-24.json
```

All commands exited zero. Receipt replay was byte-identical. The final
documentation-only wording correction preceded both receipt generations.

## Evidence And Limits

- Exact rational tests verify parity truncation, acceptance bias, the
  accepted-mixture identity, zero-amplitude contamination and resource caps.
- Independent dense exponentials test conditional-word means and the entire
  finite truncated two-generator output law, not only observed histograms.
- The sign-frustrated Jordan cycle falsifies a proposed positive-gauge shortcut.
- Tiny rational temperature `1/10^200` retains a nonzero odd probability
  without an inverse-temperature rejection loop or floating underflow.
- The live explicit 128-bit, 512-edge, degree-8 graph produced 32 outputs,
  no failures, using 3,104 words and 3,185 generator letters. It uses the
  mass bound; it is NOT a simulation of the enormous growing-degree family.
- Growing-degree family rows check parameter bounds only and explicitly
  record `input_constructed: false`.
- The cluster-derived ratio bound remains dependent on the preceding local,
  unreviewed cluster proof. Small dense controls do not prove that theorem.
- No coherent preparation, parent-gap theorem, hardness or speedup is claimed.

## SHA-256

```text
7c267615bf27a2c942f42a5981e208eaec70002dc7b9dd18b84fc49985a47286  sign_sampler.py
c4bc656637120206c13530f15179b4f902724b9a32c094e2aa8ebb1f4ba1f1df  test_sign_sampler.py
84f76da8bbc550aea2fb523ee82a729d204b6484701a7ca27923b130e979e483  SIGN_SAMPLER.md
e1905e0e92b8dab3b421fc5c21bdac9711671b6fb98c7d07f97ec22e37823d38  HANDOFF.md
```

The intended Developer checkout is still absent and the migration status
still says `needs_inspection`. Original repository tests, qsearch validation,
CLI/registry/UI integration, Git commit and push were NOT run or modified.

