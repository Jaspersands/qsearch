# Verification: 2026-10-25

37 focused tests PASS. The combined three-bundle suite has 106 passing
tests. Three new Python syntax checks PASS. Both deterministic live replay
modes PASS after all final source changes.

Commands from this directory:

    /opt/anaconda3/bin/python -m pytest -q
    /opt/anaconda3/bin/python -m pytest -q test_rational_thermal.py ../hdqi-transfer-word-sampler-2026-10-25/test_word_sampler.py ../hdqi-hidden-mode-access-2026-10-25/test_mode_access.py
    /opt/anaconda3/bin/python -m py_compile rational_thermal.py test_rational_thermal.py replay.py
    /opt/anaconda3/bin/python replay.py write
    /opt/anaconda3/bin/python replay.py check

Receipt SHA256:
ce694d62fdb30385174451a8d5224708dbd03bd6eff00b93f53e1fcca4ac9d49

## Live Certificates

Native path-power inputs use m=N^2,R=N-1,beta=1,error=.01, J=1.

| m | Modes | Blocks | Multipole order | Transfer degree bound |
|---|---|---|---|---|
| 16 | 4 | 15 | 19 | 570 |
| 64 | 8 | 18 | 20 | 720 |
| 256 | 16 | 21 | 22 | 924 |
| 1024 | 32 | 24 | 23 | 1104 |

For m=1024 the uniform scalar error certificate is <=2.227e-5 and the
squared full-state approximation bound <=1.587e-8. This is NOT a run of
the associated full sampler: its conservative bond would be 32^1104.

A separate huge-interval certificate represents more than 10^15 effective
poles with fewer than 60 blocks. Their moments are computed algebraically,
not by enumerating those poles. The small polynomial-export control has
degree 88 and specifies 542 bits of complex-root disk radius precision.
It does not compute those disks. Integer coefficients are stored as hex
strings to avoid decimal serialization digit limits.

## What Was Tested

- Exact power sums and block moments against direct finite sums.
- Rational pi bounds against a high-precision independent numerical check.
- Exact component error allowances and positive denominators.
- High-precision grids as controls, NOT as the proof of uniform accuracy.
- Exact oddness and exact polynomial-to-rational-function identities.
- Full native pilot vectors against the dense thermal reference.
- Root-precision inequalities, explicit unimplemented flags, and rejection
  of a changed approximation record before issuing a norm-bound plan.

The mathematical upper bound relies on the written derivation and cited
ECF/transfer/root-isolation premises. It is not proof-assistant checked or
independently reviewed. Tests do not establish novelty or asymptotic
advantage. Certified complex root disks and conjugate exact-factor sampling
remain unimplemented.

No main/staging, qsearch CLI/UI, registry, Git, migration or automation edits.
Main qsearch validation was not run. Ten Python files across these three
bundles passed syntax checks; there is no new JavaScript. No owned research
subprocess remains. Goal ACTIVE.
