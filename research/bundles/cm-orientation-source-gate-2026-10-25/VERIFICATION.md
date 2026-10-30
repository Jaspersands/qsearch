# Verification

2026-10-25, /opt/anaconda3/bin/python. All edits are in this isolated
research bundle plus its parent checkpoint. No main/staging/Git changes.

Executed:

    python -B -W error -m pytest -q -p no:cacheprovider cm-orientation-source-gate-2026-10-25/test_cm_gate.py
    20 passed in 0.49s

    python -B -W error -m pytest -q -p no:cacheprovider cm-orientation-source-gate-2026-10-25 regular-spectrum-kernel-2026-10-25 native-input-audit-2026-10-23
    76 passed in 4.81s

All three new Python sources pass compile(..., 'exec') syntax checks,
without writing bytecode. replay.py write and replay.py check agree exactly.
Receipt SHA256:

    942593c51a1c60bb09eccc1e583b21afa9aca3d2cd6fee5cb850bcfc8f8e288c

The independent quotient-algebra enumeration in F_r[x]/(x^4+1) checks
norm-one groups at r=3,5,7,17 with orders 8,24,64,256 and projective
class counts 4,12,32,128. Frobenius-stable Lagrangian eigenline-choice
counts are 2,2,0,4. All eight permutations commuting with the fixed CM
conjugation have the five predicted torus orders.

A 127-bit-prime nonscalar unit verifies the local ambiguity without field
enumeration. Enumeration there is explicitly NOT_RUN_CAP. The conditional
independent-completion bound at auxiliary primes 17,41,73 is 1/11059200;
it is a proved counting expression, not an observed success frequency.

Scope: no actual varieties or incoming isogeny, no quantum execution,
no published-protocol break, no independent review of the new deductions,
and no novelty claim. Main tests, qsearch.py validate and node --check
were not run: no main Python/JS or registry files changed, and the main
checkout remains migration-sensitive. Nothing is left running.
