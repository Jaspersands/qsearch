# Verification And Scope

2026-10-24. CONDITIONAL code-support source reduction. The source primitive
is prior art. No independent review, new Lean theorem, compiled receiver,
quantum execution, novelty certification or speedup admission.

## Executed Checks

- 26 new tests passed in 0.15 seconds, warnings as errors, no skips.
- 202 focused external tests passed in 15.59 seconds, warnings as errors,
  no skips. The selection includes the new source, previous spectral source,
  uniform measurement, native acquisition, recursive source, quotient,
  cancellation, group bridge, core algebra and physical-channel controls.
  Unrelated HDQI/classical-filter suites were not rerun this pass.
- All three new Python files passed py_compile after the final edits.
- run_audit.py --output code_support_receipt.json completed. A fresh run
  exactly reproduced the receipt, including six local source/document/data
  hashes and four dependency hashes. literature_transfer.json parsed.
- The frozen native receipt's 50 source/document hashes still match. No
  frozen formal source changed and no Lean rebuild was claimed.
- All owned test/audit processes completed; none remains in progress.

Receipt SHA256:

    45425b525b0c994b48a4f3f4b45d3372deef59681031c4c196e380016224621b

## What Was Actually Tested

The dense growth controls implement the literal ancilla preparation,
negated controlled swaps, coarse flag measurement and failed-growth
correction. They check its restricted operator action, not just an overlap
formula. The operator residual is below 1.10e-15. Omitting correction OR
measuring the full ancilla index gives unnormalized retained-sector leakage
4/9 in the recorded fixture. These are distinct invalid implementations.

After three rejected attempts at each of two growth stages, the correct
rank-three control extracts the expected pure wedge state with trace
distance below 4.59e-16. The per-attempt probability residual is below
2.78e-16. Understating the rank returns purity 1/3, not a valid pure source.

The original F_3 Heisenberg representation and all 81 actual Rees addresses
give the correct degenerate-code hidden support, with maximum overlap
residual below 6.39e-15. A separate sparse left-regular control retains a
nonnormal order-three subgroup rather than its order-one normal core;
its overlap identity is exact rational arithmetic. That control is
classically easy and is not a research candidate.

Forty-eight finite unitary controls check the determinant overlap and
principal-angle bound. A nonuniform mixed state falsifies using this
support source for general conjugation symmetry. Additional controls verify
the r^(-r) one-shot postselection cost, correlated-bank failure, and the
rank-dependent copy lower bound with constant operator separation.

These tests can expose errors in formulas and interfaces. They do not
replace the mathematical argument or its imported quantum primitives.

## Cost Example

For the supplied arithmetic inputs r=8, B=7, M=6, ell=31, eta=1/4 and
epsilon=1/20, the plan has 56448 extracted sources and a cap of 3400 raw
copies per source: 191923200 native copies altogether. It charges up to
2247194880 controlled register swaps and 451584 original action calls.

These are loose source-resource caps for supplied parameters, NOT gate
estimates or a verified receiver instance with B=7. The planner does not
certify B, the source promises, the group contract or a hard application.
The source dimension D is not enumerated by the proposed construction.
The dense controls do enumerate bounded dimensions and are not scalable.

## Reproduce

From this directory:

```sh
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONPYCACHEPREFIX=/tmp/qsearch-code-support-pycache PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /opt/anaconda3/bin/python -m pytest -q -p no:cacheprovider -W error test_code_support.py
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONPYCACHEPREFIX=/tmp/qsearch-code-support-pycache /opt/anaconda3/bin/python run_audit.py
env PYTHONPYCACHEPREFIX=/tmp/qsearch-code-support-pycache /opt/anaconda3/bin/python -m py_compile code_support.py test_code_support.py run_audit.py
```

The focused command, from the parent directory, used the same environment
and pytest flags with exactly these files:

```text
rees-code-support-2026-10-24/test_code_support.py
rees-spectral-mixture-2026-10-24/test_spectral_mixture.py
rees-uniform-measurement-2026-10-24/test_measurement.py
rees-formal-core-2026-10-24/test_native_source.py
rees-formal-core-2026-10-24/test_recursive_source.py
rees-formal-core-2026-10-24/test_quotient_verifier.py
rees-formal-core-2026-10-24/test_cancellation_verifier.py
rees-formal-core-2026-10-24/test_group_bridge_verifier.py
rees-formal-core-2026-10-24/test_verify.py
rees-formal-core-2026-10-24/test_central_controls.py
rees-channel-2026-10-23/test_physical_channel.py
```

## Changed Files And Remaining Risk

Eight new artifacts: code_support.py, test_code_support.py, run_audit.py,
CODE_SUPPORT.md, HANDOFF.md, literature_transfer.json,
code_support_receipt.json and this verification note. The parent research
checkpoint is the only pre-existing file changed.

The primary unresolved question is usefulness: find a motivated code/gate
family with polynomial rank, the required global gap and no known simpler
learner. In particular, a large-p logical code may force rank at least p,
eliminating the intended efficient regime. This pass does not solve that.

The main Developer checkout remained absent at the final recheck. Main
Desktop/staging, CLI, registry, UI and Git were untouched. No main suite,
qsearch validate, Node check, commit or push was run. All changes are in the
external local research folder; the full research goal remains active.
