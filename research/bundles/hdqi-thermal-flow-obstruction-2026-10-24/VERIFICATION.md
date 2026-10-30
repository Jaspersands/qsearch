# Verification And Changed Files

2026-10-24. This pass ran outside the original/migrating checkout, under
/Users/jaspersands/Developer/qsearch-research-work. The intended main
Developer checkout remained absent at the live check. No original/staging,
registry, qsearch CLI, UI or Git state was changed. No new reviewer was
spawned; the one authorized Rees review was not reused. No commit or push.

## Changes

- thermal_flow.py: exact analytic star formulas, strict rational
  countercertificates and capped independent physical-matrix controls.
- test_thermal_flow.py:29 tests covering all identities, real-time and
  Gaussian averaging, countercertificate direction, small inconclusive
  cases, zero-beta controls, scope and input/exponential-execution guards.
- make_receipt.py: six physical controls, seven all-size scalar ledgers,
  rational certificates, dependency hashes and explicit scope flags.
- receipt.json: live results; no large graph or state was simulated.
- THERMAL_FLOW.md: local proof and revised research decision.
- HANDOFF.md: bounded integration instructions with correct negative scope.
- VERIFICATION.md: this ledger.

The parent RESEARCH_CHECKPOINT_2026-10-23.md also received a leading entry.
Prior hashed research bundles were not edited.

## Final Checks

Focused tests: **29 passed in0.69s**, warnings as errors, no skips.
Broad external milestone: **700 passed in15.87s**, the29 new tests plus
the previous671. This includes the orbit/OPI, capacity, norm-flat, Rees,
BPQM, HDQI and central-rank Python controls. It is NOT the entire original
repository suite, independent mathematical review or another Lean rebuild.

All three new Python files pass py_compile. The final receipt replays
byte-identically and all11 source/dependency manifest entries match.

    receipt SHA256:
    f05505fba6a5de2a4edf3344fa76abb294eb7bae66f92e6a28ab0634327a3715

The maximum identity error in the six saved physical-matrix controls was
1.422e-14. Their largest matrix dimension is256. They construct original
Pauli operators, central projectors, matrix exponentials, KMS traces and
commutators; they do not insert the predicted sector gradients as data.
An additional test integrates physical evolution with32 Hermite nodes and
checks the phase-forgotten Gaussian average independently of its formula.

Reproduce from this bundle:

    env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
      PYTHONPYCACHEPREFIX=/tmp/qsearch-thermal-pycache \
      /opt/anaconda3/bin/python make_receipt.py --output receipt.json
    env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
      PYTHONPYCACHEPREFIX=/tmp/qsearch-thermal-pycache \
      PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
      /opt/anaconda3/bin/python -m pytest -q -p no:cacheprovider -W error test_thermal_flow.py

## Strict Counterexample And Opposite Controls

At d65536, beta1/2056, beta^2(d+1)<1/64, exact rational inequalities give:

- Squared thermal-gradient amplification at t=pi/(4sqrt(d^2+1)) is
  greater than1.24713, while the proposed degree-flow upper bound is
  less than1.01243.
- The thermal defect squared ratio is greater than4.245e9, while4d is
  only262144.

These decimal displays summarize STRICT fraction comparisons in the
artifact; they are not floating-point certificates. The all-size proof
shows unbounded violations at every fixed positive, arbitrarily small
beta^2(d+1), not only these finite constants. The large rows up to
d2^32 are analytic formulas and rational certificates, not simulation.

The SAME family is inside the earlier mass-gap and classical-envelope
regimes. Reusing those results gives filtered-parent gap>=25/36 and
classical envelope ratio<=128/127. The actual Gaussian-filtered image of
this witness is suppressed, while the phase-forgotten time average grows.
Thus neither a gap obstruction nor classical hardness is established.

## Remaining Scope

The analytic proof is local and independently unreviewed. It falsifies
the attempted KMS extension of the trace real-time gradient argument,
including its phase-forgotten Gaussian mean-square step. It leaves the
original trace lemma, the actual coherent filtered commutator, the general
degree-scale parent gap, and possible useful output advantages unresolved.

No main qsearch validation, Node check, whole-repository test run, quantum
circuit execution, natural hard candidate admission or speedup is claimed.
No process started for this pass was left running.
