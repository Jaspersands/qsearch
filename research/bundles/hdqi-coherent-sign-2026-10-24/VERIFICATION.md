# Verification: Coherent Sign Construction

Date: 2026-10-24. External local research scope only.

20 new tests and all 226 preceding external controls pass: **246 total**,
warnings as errors. Two syntax checks pass. Receipt replay is byte-identical.

```sh
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONPYCACHEPREFIX=/tmp/qsearch-coherent-pycache PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /opt/anaconda3/bin/python -m pytest -q -p no:cacheprovider -W error hdqi-coherent-sign-2026-10-24/test_coherent_sign.py hdqi-sign-sampler-2026-10-24/test_sign_sampler.py hdqi-cluster-baseline-2026-10-24/test_cluster_baseline.py hdqi-relative-flow-2026-10-24/test_relative_flow.py rees-class-three-2026-10-24/test_class_three.py hdqi-parent-gap-2026-10-23/test_parent_gap.py hdqi-filtered-parent-2026-10-24/test_filtered_parent.py hdqi-gap-baseline-2026-10-24/test_gap_baseline.py
env PYTHONPYCACHEPREFIX=/tmp/qsearch-coherent-pycache /opt/anaconda3/bin/python -m py_compile hdqi-coherent-sign-2026-10-24/coherent_sign.py hdqi-coherent-sign-2026-10-24/test_coherent_sign.py
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /opt/anaconda3/bin/python hdqi-coherent-sign-2026-10-24/coherent_sign.py
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /opt/anaconda3/bin/python hdqi-coherent-sign-2026-10-24/coherent_sign.py --output /tmp/qsearch-coherent-sign-replay-2026-10-24.json
cmp hdqi-coherent-sign-2026-10-24/receipt.json /tmp/qsearch-coherent-sign-replay-2026-10-24.json
```

The working directory was `/Users/jaspersands/Developer/qsearch-research-work`.
Every command exited zero. No tests were skipped.

## What Was Checked

- Explicit small controlled prepare/phase/unprepare matrices are unitary and
  their zero-work branches equal signed conditional expectations.
- Labeled permutation histories retain the correct repeated-word multiplicity.
- The anticommuting-edge zero amplitude is exactly cancelled, unlike the
  classical squared-mean sampler's explicitly budgeted contamination.
- Dropping known signs preserves basis probabilities but changes the state;
  discarding histories without inversion leaves a mixed state.
- Independent dense exponentials test the precise finite success vector,
  its norm and its normalized state. Receipt errors are below 1.6e-9 on the
  three recorded small controls. This is not an asymptotic proof.
- Rational precision/repetition budgets, zero couplings, tiny temperature
  and refusal to use exhaustive controls at large size are covered.
- The 128-bit artifact is a resource ledger ONLY, not a quantum run. It
  reports 768 local probability entries, 640 word slots, a conservative
  823,680 ABSTRACT-rotation bound and at most 24 unamplified attempts.
  Those are not compiled physical gate/qubit counts or observed runtime.

## SHA-256

```text
e4decaffa0075a95e9612dcd44813bb91632127835cfbcfc2bfb84eaebbc40f2  coherent_sign.py
1f0b6f3a05376c9cee610329d400ded34cecd019cc551951397ab889deca9a9c  test_coherent_sign.py
00bd833987ee88c302e2dff009af8ef4b84bf4ee53a72a1423ae35244e11a53d  COHERENT_SIGN.md
34b139a4901ce55ded5abbcd915ee5ea6a4450732e70799d8472eba91746283a  HANDOFF.md
7c267615bf27a2c942f42a5981e208eaec70002dc7b9dd18b84fc49985a47286  ../hdqi-sign-sampler-2026-10-24/sign_sampler.py
84f76da8bbc550aea2fb523ee82a729d204b6484701a7ca27923b130e979e483  ../hdqi-sign-sampler-2026-10-24/SIGN_SAMPLER.md
f32572252c925e5ab6e09b74837e659c1a5206893b21ad34408e41f67cfd8d29  ../hdqi-cluster-baseline-2026-10-24/CLUSTER_BASELINE.md
```

The proof remains local and unreviewed; the cluster-derived regime inherits
the preceding proof dependency. No circuit execution, parent gap, quantum
advantage or novelty is certified. The incomplete checkout, staging, central
registry, CLI, UI and Git were untouched. Original repository validation
was not run. No additional independent reviewer was spawned.

