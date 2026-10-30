# Verification: Physical Output Sampling

Date: 2026-10-24. External research bundle only. Proofs are LOCAL UNREVIEWED.

## Tests And Commands

**353 tests passed**, warnings as errors, no skips: 26 new sampler/shortcut
controls, 295 preceding HDQI/Rees external controls, and 32 existing tests
for the reused central-rank exact row-reduction helper. Four syntax checks
pass. The live receipt replays byte-identically; all 13 source/dependency
hashes match.

Working directory: `/Users/jaspersands/Developer/qsearch-research-work`.

```sh
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONPYCACHEPREFIX=/tmp/qsearch-output-pycache PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /opt/anaconda3/bin/python -m pytest -q -p no:cacheprovider -W error hdqi-output-sampling-2026-10-24/test_output_sampling.py hdqi-output-sampling-2026-10-24/test_commuting_linear.py hdqi-decoded-observables-2026-10-24/test_decoded_observables.py hdqi-coherent-sign-2026-10-24/test_coherent_sign.py hdqi-sign-sampler-2026-10-24/test_sign_sampler.py hdqi-cluster-baseline-2026-10-24/test_cluster_baseline.py hdqi-relative-flow-2026-10-24/test_relative_flow.py rees-class-three-2026-10-24/test_class_three.py hdqi-parent-gap-2026-10-23/test_parent_gap.py hdqi-filtered-parent-2026-10-24/test_filtered_parent.py hdqi-gap-baseline-2026-10-24/test_gap_baseline.py central-rank-2026-10-23/test_central_rank.py
env PYTHONPYCACHEPREFIX=/tmp/qsearch-output-pycache /opt/anaconda3/bin/python -m py_compile hdqi-output-sampling-2026-10-24/output_sampling.py hdqi-output-sampling-2026-10-24/commuting_linear.py hdqi-output-sampling-2026-10-24/test_output_sampling.py hdqi-output-sampling-2026-10-24/test_commuting_linear.py
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /opt/anaconda3/bin/python hdqi-output-sampling-2026-10-24/output_sampling.py
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /opt/anaconda3/bin/python hdqi-output-sampling-2026-10-24/output_sampling.py --output /tmp/qsearch-output-sampling-replay-2026-10-24.json
cmp hdqi-output-sampling-2026-10-24/receipt.json /tmp/qsearch-output-sampling-replay-2026-10-24.json
```

All commands exited zero. The hash check parsed the receipt and independently
recomputed SHA-256 for every listed source and proof dependency.

## Evidence

- Fiber enumeration agrees with exhaustive label partitioning for redundant
  inputs and arbitrary small decoder tables. Rank identities are checked
  against explicit image sets, not only against the same RREF routine.
- The ENTIRE finite accepted joint law satisfies the exact rational mixture
  identity. Independent dense physical Pauli matrices and decoder-register
  sectors verify its closeness to the actual quantum output law.
- Complex phase second moments, negative couplings, Y phases, zero proposal
  probabilities, first-stage rejection and explicit failure are covered.
- One physical Z generator falsifies replacing computational-basis output
  by incoherent Bell-label sampling. The accepted left-zero probability is
  135126217/1087415698, near the thermal value, not 1/2.
- A high-rank product-Z input is refused by the generic enumerator but is
  easy. The separate commuting/linear shortcut handles it without enumeration.
- That shortcut's full left law matches independent physical density
  controls, including relations and negative Pauli phases. Uniform affine
  sampling is checked exactly on all free-bit assignments of a small system.
- A valid linear right inverse on a Z-plus-identity input gives an actual
  output different from the desired Gibbs law. The shortcut reproduces the
  former; tests forbid treating BDB=B as a Gibbs-accuracy certificate.

## Live Runs

The generic sampler ran on an EXPLICIT 128-physical-qubit, 129-generator
noncommuting input at beta=1/16. rank(B)=129, rank(X)=128, hence k=1 and L=2.
Its analytic C_bar is 3. With eps=1/8, delta=1/16, K=385 and T=48, it made
16 outputs with no failures, using 6,160 signed words, 1,403 letters and
81 decoder calls. The budget allows 18,480 words per output. No statevector
or amplitude oracle is used in this live core.

The independent shortcut ran on 128 physical qubits with diagonal rank 128
and 128 commuting Z generators. It produced 16 left-register outputs using
biased coins and binary linear equations, with no 2^128 enumeration. Its
finite-law TV bound is 5/128 at requested eps=1/8.

These runs establish executable scope, not accuracy by histogram or
classical hardness. The examples are not quantum advantage instances. The
statistical model assumes independent random bits; seeded runs only establish
reproducibility. Neither run is a quantum execution or general high-rank
sampling theorem.

## Own-File SHA-256

```text
c9401123d1a5d508fc66b148b3b4e88f2a81c0a62af4d4522d30cbaca5c86014  output_sampling.py
1e0341c73c1d3828fb2817eb8dd099ae17c595d716c1367390a510c8ac5f14ea  commuting_linear.py
bfb06d8c9fcfe3d6b41026a89f296fa669327a97728bec4bbff6802d16e12d60  test_output_sampling.py
e991902f57866429a9a18627536d0077fea2aa59aaaff1baa39adfd7c0e396bc  test_commuting_linear.py
928dceb3c3c8671798ad6171dff801c393225b34bd465318e4250658518ccff3  OUTPUT_SAMPLING.md
ab563d94432eb73dd5cee0bc9b2364f5b1154a1f89176dfd15ff70538349821e  HANDOFF.md
```

Seven imported source/proof hashes are in receipt.json. Earlier bundles
were not modified. Original repository tests, qsearch validation, Node/UI
checks, integration, commits and pushes were NOT run. The intended Developer
checkout remains absent, and migration still says needs_inspection. No
additional reviewer was used; all changes are in this eight-file external
bundle and the checkpoint.

