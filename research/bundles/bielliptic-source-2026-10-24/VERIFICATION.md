# Verification

2026-10-24. All commands below completed. No process was left running.

## Focused Tests

From /Users/jaspersands/Developer/qsearch-research-work:

```sh
env PYTHONDONTWRITEBYTECODE=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
  /opt/anaconda3/bin/python -m pytest -q \
  bielliptic-source-2026-10-24/test_bielliptic.py \
  source-pullback-2026-10-23/test_pullback.py \
  frobenius-residual-2026-10-23/test_residual.py \
  source-residual-algebra-2026-10-24/test_residual_algebra.py \
  kernel-output-2026-10-23/test_kernel_output.py \
  scalar-cancellation-2026-10-23/test_scalar_cancellation.py \
  -p no:cacheprovider -W error
```

Final result: **225 passed in 51.56 seconds**, no skips, warnings as errors.
This includes 47 new controls and 178 direct/related dependency tests.
The earlier 221-test run preceded four additional quaternion-unit controls;
the final 225-test run supersedes it.

## Syntax And Recorded Workflow

From this bundle:

```sh
/opt/anaconda3/bin/python -m py_compile \
  bielliptic.py audit_controls.py test_bielliptic.py replay.py
/opt/anaconda3/bin/python replay.py --output receipt.json
/opt/anaconda3/bin/python replay.py --verify receipt.json
shasum -a 256 receipt.json
```

All four Python files compile. A fresh replay exactly matches the recorded
JSON and all twelve local/dependency hashes. The twelve source hashes in
the preceding source-residual-algebra receipt also still match their files.
The receipt SHA256 is

    8e022ab20a6ae322e657d35fd048f82e833ffcc35b520659cc10f9fe11509a76

The receipt records actual split-sextic map discovery over F13 and the
127-bit prime 2^127-1, exactly 120 triple candidates each. Both quotient
maps were checked on all 18 F13-rational curve points; the large-prime
control does NOT enumerate curve points. The order-four falsifier really
maps the chosen point to its hyperelliptic conjugate on the second step.

The rank-zero/rank-one/rank-two censuses are 16/0/24 at ell=3, 36/0/120 at
ell=5, and 64/0/336 at ell=7. These are abstract vector-space controls, not
measured success frequencies for native isogenies. Both arithmetic source
controls recover exact pullbacks from auxiliary levels 3,7,13 (CRT modulus
273). Rank two matches the reference kernel. Rank zero retains 36 symbolic
line pairs. Each restricted SL2 control uses 120 OPAQUE reference calls and
six orbit labels; it is not a real source or a quantum receiver.

The proof-level elliptic reduction is supported by quotient-equation
identities, integral source embeddings, exact degree/norm calculations and
odd/even mask controls. It is not independently reviewed or formally
verified. The curve controls and product-target quaternion controls have
NOT been connected into one native weak surface-isogeny experiment.

## Scope Boundaries

Eight research files in this external bundle, plus the parent checkpoint,
were created/updated. The intended Developer repository checkout was still
absent on the current check. The Desktop checkout, staging copies, existing
research bundles, CLI/UI, central registries, Git and migration state were
not edited. No additional reviewer was used.

No full-repository tests, qsearch validate, node check, website validation,
geometric torsion execution, coherent compilation, quantum execution,
cryptographic break or speedup were claimed. The broader research goal
remains active. HANDOFF.md identifies the specific missing geometry work;
it does not turn that gap into a completed implementation.
