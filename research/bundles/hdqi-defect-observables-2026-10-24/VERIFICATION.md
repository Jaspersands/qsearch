# Verification: Marked-Cluster Pauli Comparator

Date: 2026-10-24. External research bundle only. The mathematical claims
remain LOCAL UNREVIEWED and depend on the preceding local cluster proof.

## Executed Checks

**407 tests passed**, warnings as errors, no skips: 54 new controls and
353 preceding HDQI/Rees/central-rank controls. Five Python files pass
py_compile. The receipt replays byte-identically, and all 17 recorded
source/proof dependency hashes were independently recomputed without a
mismatch. No prior frozen source/proof file was edited.

Working directory: `/Users/jaspersands/Developer/qsearch-research-work`.

```sh
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONPYCACHEPREFIX=/tmp/qsearch-defect-pycache PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /opt/anaconda3/bin/python -m pytest -q -p no:cacheprovider -W error hdqi-defect-observables-2026-10-24 hdqi-output-sampling-2026-10-24/test_output_sampling.py hdqi-output-sampling-2026-10-24/test_commuting_linear.py hdqi-decoded-observables-2026-10-24/test_decoded_observables.py hdqi-coherent-sign-2026-10-24/test_coherent_sign.py hdqi-sign-sampler-2026-10-24/test_sign_sampler.py hdqi-cluster-baseline-2026-10-24/test_cluster_baseline.py hdqi-relative-flow-2026-10-24/test_relative_flow.py rees-class-three-2026-10-24/test_class_three.py hdqi-parent-gap-2026-10-23/test_parent_gap.py hdqi-filtered-parent-2026-10-24/test_filtered_parent.py hdqi-gap-baseline-2026-10-24/test_gap_baseline.py central-rank-2026-10-23/test_central_rank.py
env PYTHONPYCACHEPREFIX=/tmp/qsearch-defect-pycache /opt/anaconda3/bin/python -m py_compile hdqi-defect-observables-2026-10-24/defect_observables.py hdqi-defect-observables-2026-10-24/linear_pullback.py hdqi-defect-observables-2026-10-24/make_receipt.py hdqi-defect-observables-2026-10-24/test_defect_observables.py hdqi-defect-observables-2026-10-24/test_linear_pullback.py
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONPYCACHEPREFIX=/tmp/qsearch-defect-pycache /opt/anaconda3/bin/python hdqi-defect-observables-2026-10-24/make_receipt.py
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONPYCACHEPREFIX=/tmp/qsearch-defect-pycache /opt/anaconda3/bin/python hdqi-defect-observables-2026-10-24/make_receipt.py --output /tmp/qsearch-defect-replay-2026-10-24.json
cmp hdqi-defect-observables-2026-10-24/receipt.json /tmp/qsearch-defect-replay-2026-10-24.json
```

All listed commands exited zero. The final broad test run took 4.23 seconds.

## What The Controls Check

- Exact forest enumeration verifies the complete-graph forest count and
  the host embedding divisor, including disconnected prescribed roots.
  Wilson sampling has explicit cap failure, distinct from a zero draw.
- Exact rational proposal expectations equal an independent ordered-tuple
  marked expansion. Repeated polymers and the distinguished 1/k! factor
  are necessary; negative controls catch replacing or omitting them.
- Independent dense canonical matrices verify all twisted insertions on
  three graph types. Coupling signs, anti-Hermitian ordered words, global
  twists, odd-Y zeros, and all coefficient Pauli flip bounds are covered.
- Marked activities reconstruct the inserted partition through the
  polymer factorization, with rational Taylor error bounds. Precision
  relative to a root envelope as small as order 10^-75 is checked.
- Independent actual physical density matrices verify the linear pullback
  on redundant, noncommuting and signed/Y inputs, including every linear
  section of one rank-two redundant example. Missing syndromes give zero.
- A valid linear section preparing the WRONG Gibbs output still has the
  predicted actual expectation. Callback and invalid-matrix decoders fail
  closed; no finite testing is used to infer callback linearity.

These controls check identities and implementations. They do not substitute
for independent review of the all-size convergence, resource, or precision
arguments.

## Live Artifacts And Costs

Three rational finite cases each ran 2,048 marked-cluster diagnostic draws,
6,144 total. Their exact truncated proposal means agree algebraically with
the direct marked expansion. The absolute residuals from the full small
restricted ratios were approximately 2.78e-13, 3.99e-14 and 5.73e-15.
The SHORT-RUN MONTE CARLO MEANS HAVE NO CONFIDENCE CERTIFICATE.

The separate live algebra run constructs an explicit 128-physical-qubit,
128-generator noncommuting path input and its binary decoder. A physical
generator pulls back to one pilot Pauli without enumerating a statevector.
At beta=1/32 and epsilon=1/4096 the ledger uses excess cutoff 9 and at most
10 vertices per activity. Its deliberately loose bound asks for
15,393,162,788,864 marked draws, which were NOT executed. Polynomial time
in a theorem must not be confused with a practical implementation.

Four clique-chain family rows give an analytic lower bound on log C while
remaining in the comparator regime. The large graphs/states were NOT built.
This separates the new theorem's regime from polynomial sign cost, not
from the best classical algorithms on those structured examples.

## Exact Change Scope

New nine-file bundle:

- DEFECT_OBSERVABLES.md: proof, pricing, prior art, falsifiers and limits.
- defect_observables.py: marked forest/cluster reference, rational inserted
  activities, exact expectation controls and conservative resource plans.
- linear_pullback.py: exact verified-linear-decoder physical Pauli mapping.
- test_defect_observables.py and test_linear_pullback.py: 54 new tests.
- make_receipt.py and receipt.json: reproducible controls and 17 hashes.
- HANDOFF.md: bounded integration tasks, proof gates and unresolved work.
- VERIFICATION.md: this tested-scope record.

The external research checkpoint is updated. Original Desktop source,
migration staging, main CLI/registry/UI and Git are untouched. The intended
Developer checkout is absent and the migration status remains
needs_inspection. Main repository tests, qsearch validation, Node/UI checks,
commits and pushes were NOT run. No additional independent reviewer was
created; the previously authorized Rees review is already complete.

The general degree-scale coherent preparation/parent gap is still OPEN.
No quantum advantage, full-output sampler or nonlinear-decoder simulation
has been established by this pass.
