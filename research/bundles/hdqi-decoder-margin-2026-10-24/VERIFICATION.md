# Verification And Scope

Date: 2026-10-24. Interpreter: /opt/anaconda3/bin/python.

## Final Checks

```sh
python -m pytest -q -W error test_decoder_margin.py ../hdqi-decoded-observables-2026-10-24/test_decoded_observables.py ../hdqi-defect-observables-2026-10-24/test_defect_observables.py ../hdqi-cluster-baseline-2026-10-24/test_cluster_baseline.py ../hdqi-flux-gap-2026-10-24/test_flux_gap.py ../hdqi-fermion-sampler-2026-10-24/test_fermion_sampler.py
```

377 passed in 5.21s: 65 new and 312 dependency/context tests. No skips;
warnings treated as errors. The first 64-test run and preceding 376-test
milestone predated the stricter live precision control.

Four Python files pass py_compile after the final changes. The final
`python replay.py --write` completed, followed by a separate fresh
`python replay.py --check` matching all thirteen source hashes. The six
local science/code/handoff files and seven dependency files are covered;
the verification note and checkpoint are excluded to avoid circular hashes.
All eleven source hashes of the previous flux-gap bundle remain intact.

Receipt SHA256:

    9c6eb5bd60c557a1e752ccad200fcecf4629c7c1b7902af20c3236ceb1f814b4

## What Was Checked

- Exact integer decoder-ball checks and rational factorial-moment tails.
- Signed native thermal amplitudes against dense physical Bell pullbacks,
  with a genuinely nonlinear decoder, negative couplings and Y phases.
- All 32 word-derived physical observables on the five-cycle fixture,
  including scalar relations and out-of-image-label controls.
- Whole-column agreement for short words versus only low-weight-block
  agreement for the arbitrary-readout theorem.
- The four-cycle degree-one filter's exact expectations 1 and 1/2, proving
  that perfect decoding success does not justify the missing-margin shortcut.
- Rejection of false radius claims, inadequate error budgets, invalid
  Hermitian phases, noncentral proposed relations and exceeded audit caps.
- Exact binary construction of growing-degree native Hamiltonians with
  a repetition relation and a polynomial nonlinear majority decoder.

The live input has 496 generators and 495 physical qubits, a radius-247
repetition decoder, and cutoff 31 at requested readout accuracy 1/4096.
No 2^496 pilot or 2^495 physical Hilbert space was allocated. The phase-
preserving canonical reduction calls the existing marked-cluster planner.
Its conservative count is 61,572,651,155,456 root draws, NOT executed work
and not a claim of practical classical performance. The scalar estimate is
null, not a fabricated computed answer. The output retains conditional
decoder-proof and unreviewed-theorem statuses.

The s=1024 family has symbolic beta^2*m=2097151/1024 and
beta*d=1048575/8192. Its enormous physical input was NOT constructed. This
checks an asymptotic regime comparison, not a benchmark or hardness test.

## Not Established

No independent or formal proof; no production FPRAS execution; no joint
output sampler; no quantum circuit; no Gibbs-accuracy assertion for arbitrary
fixed-sign decoding; no novelty or speedup. The theorem depends on a genuine
uniform decoder-radius proof and the preceding local cluster-comparator
proof. An average success rate does not satisfy that premise.

The main Desktop checkout remains dirty and was read only. The intended
Developer checkout was absent at the initial live check. No main/staging,
CLI/UI, registry, Git, migration, or additional reviewer changes were made.
Full-repository validation was not run against the unverified migrating
checkout. All owned test, syntax and replay processes completed.
