# Verification: Actual Decoded Observable Attack

Date: 2026-10-24. External local research only; no central registry admission.

## Executed Checks

49 new controls and all 246 prior external controls pass: **295 tests total**,
warnings as errors, no skips. Two syntax checks pass. Receipt replay is
byte-identical after the final documentation clarification about randomness.

From `/Users/jaspersands/Developer/qsearch-research-work`:

```sh
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONPYCACHEPREFIX=/tmp/qsearch-observable-pycache PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /opt/anaconda3/bin/python -m pytest -q -p no:cacheprovider -W error hdqi-decoded-observables-2026-10-24/test_decoded_observables.py hdqi-coherent-sign-2026-10-24/test_coherent_sign.py hdqi-sign-sampler-2026-10-24/test_sign_sampler.py hdqi-cluster-baseline-2026-10-24/test_cluster_baseline.py hdqi-relative-flow-2026-10-24/test_relative_flow.py rees-class-three-2026-10-24/test_class_three.py hdqi-parent-gap-2026-10-23/test_parent_gap.py hdqi-filtered-parent-2026-10-24/test_filtered_parent.py hdqi-gap-baseline-2026-10-24/test_gap_baseline.py
env PYTHONPYCACHEPREFIX=/tmp/qsearch-observable-pycache /opt/anaconda3/bin/python -m py_compile hdqi-decoded-observables-2026-10-24/decoded_observables.py hdqi-decoded-observables-2026-10-24/test_decoded_observables.py
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /opt/anaconda3/bin/python hdqi-decoded-observables-2026-10-24/decoded_observables.py
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /opt/anaconda3/bin/python hdqi-decoded-observables-2026-10-24/decoded_observables.py --output /tmp/qsearch-decoded-observables-replay-2026-10-24.json
cmp hdqi-decoded-observables-2026-10-24/receipt.json /tmp/qsearch-decoded-observables-replay-2026-10-24.json
```

Every command exited zero. Tests compare exact finite rational moments with
an independently assembled physical density matrix, including the decoder
register trace, ordered physical Pauli products and complex Y phases.

## Decisive Controls

- Actual outputs with redundant physical generators, negative couplings,
  correct representative decoders and bad decoders.
- Every two-generator decoder table gives a partial involution, without
  assuming that its outputs have the supplied syndrome.
- One- and two-physical-qubit cases include out-of-image observable labels.
- Exact second-moment bounds survive rare weights greater than 10^50;
  clipping those weights demonstrably biases the estimator.
- Rational square-root weights are downward and relatively accurate on
  inputs as large as 10^200 and as small as 10^-200.
- Insufficient draw budgets refuse certification. Synthetic aggregation
  fixtures cover successful median division and denominator refusal; those
  synthetic fixtures are NOT shortened certified physical experiments.

## Live Workflow Scope

The live run made 128 diagnostic draws, consuming 384 sampled words and
153 generator letters. Its receipt explicitly records `certified_estimate:
false`. Exact finite-law moments are recorded separately from sample means.

The conservative eps=1/8, delta=1/16 theorem configuration requires
115,605,504 draws, at most 346,816,512 words. That full estimator was NOT
run. No high-confidence empirical output claim is based on the short run.
The theoretical polynomial claim depends on the local proof and independent
random-bit premise, not the seeded diagnostic or the finite tests.

## SHA-256

```text
f4cda5ea5f0ba9dbaf712d5b7e5958ee8cf438f2cfaf4c017cb1197368137f71  decoded_observables.py
b5a99f0a2375b2ba9b526795d8a0f4ecd7726b01adc80cf2371ce9eb02556804  test_decoded_observables.py
f11a7eeedfbe07e4bcb21e5aca7be10ed92591024464761623cff0716826819a  DECODED_OBSERVABLES.md
98654b77a05e47d3e01b54ec9fc8b78303648a4f72316fad50d0ad502cc469a1  HANDOFF.md
```

The receipt also hashes its two coherent-sign and two classical-sign source
dependencies. Earlier frozen bundles were not changed.

No full-output sampler, Gibbs approximation, universal dequantization,
parent-gap theorem, novelty certification or quantum speedup is claimed.
Original repository tests, qsearch validation, UI checks, integration and
Git operations remain unperformed because the intended local checkout is
absent and cloud migration still needs inspection. No new reviewer.

