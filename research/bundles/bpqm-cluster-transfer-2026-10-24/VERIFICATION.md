# Verification: Classical Cluster Mobility

Date: 2026-10-24. External workspace only. Local mathematical derivation,
not independent review, formal proof-assistant verification or speedup admission.

## Checks Executed

**464 tests passed**, warnings as errors and no skips: 57 new controls plus
the preceding 407 HDQI/Rees/central-rank controls. The broad run took 5.23s.
Three Python files pass py_compile. The live receipt replays byte-identically.
All six recorded source/dependency hashes and the separate entropy-certificate
hash were recomputed and match. All required owned processes have completed.

The entropy witness has 98 intervals covering [1/50,1], with **196 exact
rational endpoint comparisons**. Numerical proposals never certify an endpoint;
the separate verifier reads the frozen JSON and checks inequalities and coverage.
It rejects false overlaps, false decay rates, missing intervals and bad witnesses.

Controls cover rank defects, duplicate and zero rows, c=0, the Gram/coset
identity, exact joint TV, detailed balance, stationary displacement laws,
whole-history transfer, different retention at a nonstationary fixed start,
exponential gauge-rejection cost, and nullity-versus-Hamming-mobility confusion.
The socket coefficient is checked by enumerating all marked socket positions
of a small regular instance, independently of the generating-function routine.
Binary kernels are checked against exhaustive enumeration and the existing
prime-field RREF implementation. A 512-spin test forbids state enumeration.

## Live Work And Scope

The receipt includes 48 seeded matrix/retention diagnostics, 16 each at n=128,
512 and 2048 spins. They use unconditioned regular socket matching, retain
parallel mod2 cancellations, and sample retained equations with probability
13/20. Active-coordinate ranges were respectively 0..2, 0..3, and 1..10;
sampled Hamming jumps were 0..2, 0..2, and 0..8. None exceeded n/50.
These 48 observations are NOT a tail estimate or confidence certificate.

The proven local ensemble bound, not those observations, gives less than
1.333e-10 at n=4096 and 7.056e-28 at n=8192. These large rows are analytic
bounds; no 4096/8192-spin quantum experiment was run. Every numerical
UNIFORM-DISORDER transfer remains None/UNKNOWN because a finite-block
quantum error theorem has not been supplied. No Gibbs-state enumeration or
quantum statevector is used by the scalable path.

## Reproduction Commands

From `/Users/jaspersands/Developer/qsearch-research-work`:

```sh
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONPYCACHEPREFIX=/tmp/qsearch-cluster-transfer-pycache PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /opt/anaconda3/bin/python -m pytest -q -p no:cacheprovider -W error bpqm-cluster-transfer-2026-10-24/test_cluster_transfer.py hdqi-defect-observables-2026-10-24 hdqi-output-sampling-2026-10-24/test_output_sampling.py hdqi-output-sampling-2026-10-24/test_commuting_linear.py hdqi-decoded-observables-2026-10-24/test_decoded_observables.py hdqi-coherent-sign-2026-10-24/test_coherent_sign.py hdqi-sign-sampler-2026-10-24/test_sign_sampler.py hdqi-cluster-baseline-2026-10-24/test_cluster_baseline.py hdqi-relative-flow-2026-10-24/test_relative_flow.py rees-class-three-2026-10-24/test_class_three.py hdqi-parent-gap-2026-10-23/test_parent_gap.py hdqi-filtered-parent-2026-10-24/test_filtered_parent.py hdqi-gap-baseline-2026-10-24/test_gap_baseline.py central-rank-2026-10-23/test_central_rank.py
env PYTHONPYCACHEPREFIX=/tmp/qsearch-cluster-transfer-pycache /opt/anaconda3/bin/python -m py_compile bpqm-cluster-transfer-2026-10-24/cluster_transfer.py bpqm-cluster-transfer-2026-10-24/test_cluster_transfer.py bpqm-cluster-transfer-2026-10-24/make_receipt.py
env PYTHONPYCACHEPREFIX=/tmp/qsearch-cluster-transfer-pycache /opt/anaconda3/bin/python bpqm-cluster-transfer-2026-10-24/make_receipt.py --write
env PYTHONPYCACHEPREFIX=/tmp/qsearch-cluster-transfer-pycache /opt/anaconda3/bin/python bpqm-cluster-transfer-2026-10-24/make_receipt.py --output /tmp/qsearch-cluster-transfer-replay-2026-10-24.json
cmp bpqm-cluster-transfer-2026-10-24/receipt.json /tmp/qsearch-cluster-transfer-replay-2026-10-24.json
env PYTHONPYCACHEPREFIX=/tmp/qsearch-cluster-transfer-pycache /opt/anaconda3/bin/python bpqm-cluster-transfer-2026-10-24/make_receipt.py --verify-certificate bpqm-cluster-transfer-2026-10-24/entropy_certificate.json
```

All listed checks exited zero. An initial ad hoc hash-check command used a
relative Path parent incorrectly; rerunning with Path.cwd() checked all hashes.
This was a verification-command path error, not an artifact mismatch.

## Changes And Untouched State

New eight-file bundle: CLUSTER_TRANSFER.md, cluster_transfer.py,
test_cluster_transfer.py, make_receipt.py, HANDOFF.md, entropy_certificate.json,
receipt.json and this verification record. The external research checkpoint
was updated. Earlier frozen bundles were not edited.

The intended Developer checkout is still absent. Migration remains
needs_inspection; the Desktop original and staging were not modified.
No main CLI/registry/UI changes, main-repository tests, qsearch validate,
Node checks, commits or pushes were performed. The user-authorized Rees
review was already completed; no additional reviewer was spawned here.

Next: the native regular Gibbs geometry or a constructive rapid-mixing
mechanism, not another trajectory scan. The small-step theorem by itself is
compatible with polynomial mixing and says nothing about all classical methods.
