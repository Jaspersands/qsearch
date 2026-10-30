# Verification: 2026-10-25

Interpreter: /opt/anaconda3/bin/python, Python 3.13. Environment versions
and five source hashes are stored in receipt.json.

Executed from this bundle:

    /opt/anaconda3/bin/python -m pytest -q
    /opt/anaconda3/bin/python -m py_compile mode_access.py controls.py test_mode_access.py replay.py
    /opt/anaconda3/bin/python -u replay.py write
    /opt/anaconda3/bin/python -u replay.py check

Final result: 44 tests PASS; four syntax checks PASS; live write/check PASS
for 16 exact certificate cases and eight separate floating controls.

Receipt SHA256:
616b57bda5a4d4f2d2655b953342f9a0a9d4b13eb83031a3d46e000f420387b1

## Results

Growing-range instances use m=N^2, R=N-1, ell=N, J=1, beta=1, error=1/100.
The following decimals summarize exact rational enclosures; they are not
fitted asymptotic exponents.

| N | m | Active/total modes | Active gap lower | Active overlap lower |
|---|---|---|---|---|
| 4 | 16 | 4/4 | 1.16349 | 0.345189 |
| 8 | 64 | 8/8 | 0.412910 | 0.0989701 |
| 12 | 144 | 12/12 | 0.141444 | 0.0319508 |
| 16 | 256 | 16/16 | 0.0491217 | 0.0107798 |
| 24 | 576 | 24/24 | 0.00601830 | 0.00128594 |
| 32 | 1024 | 31/32 | 0.0193668 | 0.00303707 |

The N=32 omitted-state distance bound is about 0.000185457. This local
improvement in retained conditioning comes from omitting one mode, not
evidence of polynomial active conditioning for all sizes.

Six dense full-state controls have maximum full-TFD vector discrepancy
2.42e-15. Two finite-midpoint-filter plus dense-polar controls have vector
errors 5.10e-7 and 2.32e-7. They validate relative phases and composition,
not a quantum circuit or rigorous floating-point error estimate.

The exact small-overlap controls charge exponential inverse overlap for
J=(2^-b,1), ell=1, b in {4,12,32}, despite a constant frequency gap; ell=2
removes this particular obstruction. The thermal tests reactivate a weak
mode at beta=4096. A seven-generator input J=1/1100 shows the squared
omission bound fits the budget when the linear one does not.

## Corrections During This Pass

- A long unlogged exploratory sweep was terminated and replaced by a
  checkpointed replay. No result is claimed from the terminated run.
- Reciprocal powers in the residue formula were cancelled symbolically
  before exact interval evaluation. This changes verifier conditioning,
  not the charged quantum resources. Equivalence tests pass.
- The squared-omission test exposed insufficient energy precision in a
  DENSE reference when every production mode was omitted. Dense controls
  now independently request 128-bit intervals. The old in-flight replay
  failed its CAR check; it was not accepted. All final tests and both
  complete replays were rerun after the correction.

## Scope

No main-checkout, staging, CLI/UI, registry, Git, or migration edits.
Main qsearch validation and node checks were not run because this is an
isolated research bundle and no JavaScript changed. No commit/push or
background automation was created. The verified-main destination remains
absent. No process from this completed bundle remains running.

The thermal construction is a written conditional derivation, not formally
checked or independently reviewed. Circuit compilation, uniform active
conditioning, matched classical full-output complexity, useful reduction,
and novelty remain unresolved. The research goal remains active.
