# Verification

2026-10-24. External research bundle only; no main-repository changes.

## Executed Commands

From /Users/jaspersands/Developer/qsearch-research-work:

```text
/opt/anaconda3/bin/python -m pytest -q -W error -p no:cacheprovider \
  hdqi-paired-positivity-2026-10-24/test_paired_positivity.py \
  hdqi-offline-tangent-2026-10-24/test_offline_tangent.py \
  hdqi-defect-observables-2026-10-24/test_defect_observables.py \
  hdqi-defect-observables-2026-10-24/test_linear_pullback.py \
  hdqi-cluster-baseline-2026-10-24/test_cluster_baseline.py
168 passed in 1.61s
```

This includes 32 new tests and 136 related predecessor tests, warnings as
errors, no skips. From this bundle directory:

```text
/opt/anaconda3/bin/python -m py_compile \
  paired_positivity.py test_paired_positivity.py run_audit.py
PASS, exit 0

/opt/anaconda3/bin/python run_audit.py
PASS, receipt.json generated
```

A fresh independent replay matched saved JSON exactly. All nine current
source/dependency hashes and all ten hashes in the preceding offline-tangent
receipt matched their actual files. Receipt SHA256:

```text
8ee335c4972dd7a5a7ebfd6fc5cb78e6e5040969846bbae7ab5ec99c2b86ded0
```

## What The Checks Establish

- Exact leading colored coefficient -2/2025 at time power 12, with positive
  sum after all output labels are combined. Uncolored aggregation loses
  the obstruction.
- Independent integer matrix powers, multivariate rational recurrence and
  literal enumeration of 360 words agree: 188 positive and 172 negative
  words give the path amplitude coefficient 1/45.
- The signed coefficient-space automorphism is orthogonal, commutes with
  the full Hamiltonian, fixes the vacuum, and negates label 30. The general
  algebra argument supplies the all-time zero; finite powers alone do not.
- Rational Taylor intervals are strictly negative at beta=1/32, 1/64 and
  1/512. The analytic remainder inequality separately proves negativity
  throughout 0<beta<=1/32, not just at the three points.
- Vertex relabeling preserves the leading negative weight. Connected
  128- and 1024-vertex extensions preserve the supplied symmetry and degree
  three, verified symbolically without statevectors.
- Guards reject large dense powers, invalid automorphisms, duplicate edges,
  mismatched support/labels and uncontrolled Taylor tails.

The clipping-amplification ledger requires approximately 1.25e25 disjoint
blocks for the displayed conservative constant-error bound. It is an
asymptotic warning, not a practical executed instance or a connected-family
TV bound. No full-output sampler was implemented.

## Scope Limits

No full main-repository test suite, node check or qsearch validate was run:
the main checkout remains outside the edited scope during unverified
migration. No CLI, registry, UI, Git, migration, or frozen bundle was changed.
No new independent reviewer, Lean check, quantum run, novelty certification
or generic classical hardness claim. All owned processes completed.
