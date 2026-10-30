# Verification And Scope

2026-10-24. The mathematical reduction is local and conditional. These
checks do not constitute an independent review, a Lean proof, a compiled
spectral preprocessor, a quantum execution or a classical speedup.

## Executed Checks

- 21 new tests passed in 0.10 seconds, warnings as errors, no skips.
- The expanded external selection passed 1048 tests in 46.51 seconds,
  warnings as errors, no skips. This is exactly the 1027-test selection
  documented in ../rees-uniform-measurement-2026-10-24/VERIFICATION.md plus
  this directory's test_spectral_mixture.py. It is not the main repo suite.
- py_compile passed for spectral_mixture.py, test_spectral_mixture.py and
  run_audit.py.
- run_audit.py --output spectral_mixture_receipt.json completed. A fresh
  execution exactly reproduced the receipt after the final source-note edit.
- All four recorded new source/document hashes and both dependency hashes
  match. The frozen native-source receipt's 50 source/document hashes and
  five prior receipt hashes also match.
- No frozen Lean source changed. The previous 180-theorem/283-declaration
  Lean audit was not rerun, expanded or credited to this new argument.

Receipt SHA256:

    142f3a0494096c6e22e29eec6f92fe7383188cc22769dbe28c1a21bc4a280ddd

## Decisive Controls

On the genuine F_3 Heisenberg representation and all 81 actual Rees-cover
elements, the matched spectral packet has maximum overlap error below
2.61e-15. The conjugation stabilizer has order 9; the old scalar-support
stabilizer has order 3. They are not the same task.

Replacing the matched packet with independent mixed marginals yields
hidden-element overlap error 26/27. For the degenerate state I/3, a genuine
conjugation symmetry instead has matched-basis-packet overlap zero. Both
invalid extensions are explicitly rejected.

A principal-eigenvector-only approach misses an order-three operation that
changes the mixed state by trace distance approximately 0.08660. Another
order-three control has leading-eigenstate overlap gap about 8.94e-8 but
mixed distance about 0.08660. The argument therefore uses an aggregate
mixed-state gap, not an assumed gap for every individual eigenstate.

Literal controlled partial-SWAP channels include an entangled reference.
Their errors decrease from 0.22842 at one step to 0.01594 at sixteen steps,
below the derived 2t^2/N bound for t=0.7. These finite controls do not prove
a diamond-norm bound; the separate complete-channel derivation does that
conditionally on the specified gates and independent input copies.

The exact one-attempt cap example has abort mass 664/729 and conditions
spectral weights to (64/65,1/65), not (2/3,1/3). All such aborts are charged;
no normalized-success distribution is silently substituted.

## Resource Meaning

The deliberately loose example plan has 9408 packets, 11299008 spectral
measurements, 45 phase bits per measurement and a total raw-copy cap

    6068920750434573593231562563612985514850543808.

This enormous upper bound establishes neither practicality nor optimality.
It makes the polynomial dependence on the supplied weight, spectral-gap,
orbit-gap and global-error parameters explicit. It does not certify those
promises, the receiver leaf cap, or a natural hard instance distribution.

## Reproduce

Run in this directory:

```sh
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONPYCACHEPREFIX=/tmp/qsearch-spectral-mixture-pycache PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /opt/anaconda3/bin/python -m pytest -q -p no:cacheprovider -W error test_spectral_mixture.py
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONPYCACHEPREFIX=/tmp/qsearch-spectral-mixture-pycache /opt/anaconda3/bin/python run_audit.py
env PYTHONPYCACHEPREFIX=/tmp/qsearch-spectral-mixture-pycache /opt/anaconda3/bin/python -m py_compile spectral_mixture.py test_spectral_mixture.py run_audit.py
```

## Files And Checkout

New: SPECTRAL_MIXTURE.md, spectral_mixture.py, test_spectral_mixture.py,
run_audit.py, spectral_mixture_receipt.json, HANDOFF.md and this report.
The parent research checkpoint is the only existing file updated.

All writes are outside iCloud. The intended main Developer checkout is
still absent. Main/staging, CLI, registry, UI and Git were untouched. No
main suite, qsearch validate, Node check, commit or push was attempted.
All owned test/audit sessions completed. The broader research goal remains
active; a natural useful application and novelty remain unresolved.
