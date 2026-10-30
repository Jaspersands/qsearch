# Verification

2026-10-24. Everything here ran outside the migrating Desktop checkout.

## Commands And Outcomes

From /Users/jaspersands/Developer/qsearch-research-work:

```text
/opt/anaconda3/bin/python -m pytest -q -W error -p no:cacheprovider \
  hdqi-offline-tangent-2026-10-24/test_offline_tangent.py \
  hdqi-defect-observables-2026-10-24/test_defect_observables.py \
  hdqi-defect-observables-2026-10-24/test_linear_pullback.py \
  hdqi-cluster-baseline-2026-10-24/test_cluster_baseline.py
136 passed in 1.72s
```

This includes 46 new tests and 90 direct-dependency tests, with no skips.
From the new bundle directory:

```text
/opt/anaconda3/bin/python -m py_compile \
  offline_tangent.py test_offline_tangent.py run_audit.py
PASS, exit 0

/opt/anaconda3/bin/python run_audit.py
PASS, receipt.json generated
```

Independent fresh receipt replay matched the saved JSON exactly. All ten
local/dependency hashes matched; all seventeen hashes from the frozen
defect-observable predecessor receipt also matched. Receipt SHA256:

```text
27327b2fc1c9a67b68f5bd392b383d7700f48cc3200b089268b6618aff8d7cf6
```

## Observations, Not Algorithmic Evidence

The full-patch four-qubit TFD controls at 8,16,32 steps had vector errors
0.0020299123, 0.0009041404, 0.0004283280. Their exact tangent residual was
below 9.1e-16. This validates the algebra and first-order endpoint behavior
on those controls; it uses exponentially costly exact target access.

A restricted-patch control had tangent residual 0.152763 and final error
0.0247168, within its explicit accumulated bound 0.0810754. It is not evidence
that correlation decay holds on a useful asymptotic graph family.

The singular-polar counterexample has density trace change 4e-12, generator
operator change 0.800000000004, and cross-objective excess about 3.2e-12.
This refutes the tempting operator-continuity argument without refuting
the action-error lemma. A separate exact control shows that zero single-site
far covariances do not imply zero joint far covariance.

All 512 paired Pauli/graph combinations in the two-vertex Clifford test
agree, including Y signs and zero-ancilla sectors. The 128-vertex symbolic
pullback ran without a statevector. Large moment-count/ball rows are ledgers
only, not executed tomography, classical FPRAS calls, or quantum gates.

## Boundaries

No full-repository pytest, node check or qsearch validate was run because
no main-repository code, CLI, UI, or registry was modified. No production
observable estimator, quantum preparation, independent reviewer, new Lean
check, novelty review, or speedup certificate was executed. The exact local
covariance requirement remains a proof dependency. All owned processes
completed. No Git changes were made in the main checkout.
