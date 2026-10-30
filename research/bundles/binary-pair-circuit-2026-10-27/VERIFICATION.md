# Verification And Scope

2026-10-27. The local construction, conditional resource argument and
qualified sampling bound are independently reviewed. No novelty, quantum
execution, classical separation or Shor-level algorithm is established.

## Executed Tests

The final combined suite passes **594 tests in16.17s**, no skips, with
warnings treated as errors. This comprises95 new controls here and the499
tests listed in ../affine-resampling-audit-2026-10-27/VERIFICATION.md.
The exact invocation, from the parent directory, is:

```sh
env PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONPYCACHEPREFIX=/tmp/qsearch-review-pycache /opt/anaconda3/bin/python -m pytest -q -p no:cacheprovider -W error \
  binary-pair-circuit-2026-10-27/test_pair_circuit.py \
  affine-resampling-audit-2026-10-27/test_repair.py \
  small-prime-tower-2026-10-27/test_small_prime.py \
  systematic-full-support-2026-10-27/test_systematic.py \
  constructive-tower-2026-10-27/test_source_controls.py \
  one-point-plane-adapter-2026-10-26/test_plane_control.py \
  compressed-graded-algebra-2026-10-26/test_compressed_control.py \
  auxiliary-four-list-2026-10-26/test_four_list.py \
  prime-sampler-halving-2026-10-26/test_sampler_contract.py \
  matrix-geometry-lift-2026-10-26/test_point_lift.py \
  ag-divisor-class-control-2026-10-26/test_divisor_control.py \
  usd-review-resolution-2026-10-26/test_resource_bounds.py \
  generic-divisor-class-2026-10-26/test_class_bound.py \
  prime-ag-tower-source-2026-10-26/test_tower_source.py \
  ag-affine-sampling-2026-10-26/test_affine_sampling.py \
  unambiguous-reduction-2026-10-26/test_usd_reduction.py \
  schur-growth-classical-gate-2026-10-26/test_schur_gate.py \
  inverse-trace-local-list-2026-10-26/test_local_list.py \
  inverse-trace-modular-norm-2026-10-25/test_modular_norm.py \
  inverse-trace-norm-transfer-2026-10-23/test_norm_transfer.py \
  inverse-trace-residual-2026-10-23/test_residual_sat.py
```

Five-file syntax check passes:

```sh
env PYTHONPYCACHEPREFIX=/tmp/qsearch-review-pycache /opt/anaconda3/bin/python -m py_compile pair_circuit.py transfer_control.py sampling_bounds.py test_pair_circuit.py replay.py
```

Coverage includes interval preparation/inversion and padding; exhaustive
small reversible comparison; all68 labels at q2,3,4,5,7,8,9,13,17; complex
zero-sum superpositions; full padded-space inverses; direct phi_0 preparation;
wrong unsigned, padded-uniform, omitted-phase and bitwise-SWAP controls;
large symbolic plans without state allocation; coherent error budgets;
exact rational conditioning and square-root bounds. The review's analytic
inverse-pair dirty-work probability1-2/q is replayed at q2,3,5,9.

The accepted-transfer test uses the actual binary inverse with shared work
retained. Its decoder-success projector is a bounded enumeration, NOT a
general compiled Gaussian-elimination circuit. Tests cover lengths2,3 and
three syndromes. Live replay additionally covers length4, at19 qubits.
It records validity, joint fidelity, dirty work and conditional output TV.
The numerical controls are deliberately easy consistency checks, not
candidate problems or speedup benchmarks.

Final replay --write and --check pass for68 labels and nine transfer cases.
Receipt SHA256:
`261ff4f8ffa9912b17c4ff9a6f3f29767ab2546647143d248e829ff32ffa18d8`.
The receipt includes final implementation, proof and independent-review
provenance hashes. Its scalar source-precision example is not a certified
native success bound.

## Independent Review

../pair-circuit-review-2026-10-27/REVIEW.md reconstructs the map, reversible
comparison, interval recursion, inverse counterexample, finite-set resource
argument and conditional sampling bound. It found no fatal flaw, and points
out max-controls<=max(n,3), dirty inverse work, raw-success accounting,
explicit finite-field representation and the intrinsic sampling-error floor.
Its primary synthesis references are included. The reviewer did not rerun
the parent tests. It completed and was closed after its findings were read.

The separate literature/usefulness review is complete. It demotes the
family-level claim: DFS24 supplies the essential exact-herald antecedent,
and the matrix-only Schur locator supports ordinary DQI on the same AG input,
including ideal exact conditional uniform sampling. This is not classical
full-support dequantization. The review is preserved in the receipt.

The follow-on locator pass reran this suite plus17 new tests:611 PASS in16.45s.
See ../schur-locator-decoder-2026-10-27/VERIFICATION.md for the final scope.

## Repository Boundary

Main `/opt/anaconda3/bin/python -B qsearch.py validate` passes with validtrue
and issues[]. Full main-repository tests were NOT run. No root index.js
exists in that checkout and no UI files were changed; no node check is claimed.
No CLI wiring, central registry promotion, commit/push or storage migration.

The new executable bundle remains in the local Developer research directory,
outside Git. Repository checkpoint pointers are not a portable backup. A later
selected import must preserve these reviewed sources and provenance and rerun
the receipt. Do not import every isolated research directory indiscriminately.

No general reversible decoder, finite-gate compiler, actual large-field
quantum execution, generic higher AG source, useful-problem reduction or
classical uniform-sampling lower bound was implemented by this pass.
