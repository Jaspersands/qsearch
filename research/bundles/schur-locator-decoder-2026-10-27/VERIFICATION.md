# Verification

2026-10-27. This is a matrix-only classical SPARSE-ERROR decoder and an
ordinary-DQI comparison. It is not a classical full-support search/sampling
algorithm and is not evidence for a new quantum speedup.

## Executed

17 focused tests passed in0.71s. The subsequent combined research suite
passed **611 tests in16.45s**, no skips, warnings treated as errors. This is
the exact594-test invocation in
../binary-pair-circuit-2026-10-27/VERIFICATION.md with
`schur-locator-decoder-2026-10-27/test_locator.py` added. It is not the full
main-repository suite.

The tests exhaust all F5 degree-one codewords with every single-symbol
error; exercise two-error RS cases; decode the real43-by-176 AG matrix,
including changed row basis, column permutation and nonzero scalings; and
check fail-closed behavior when promises or the requested radius fail.
Native errors have weights0,1,8,9. The all-error-pattern statement rests on
the written locator proof, not these controls. Distances are source-theorem
promises, not values computed by an efficient general minimum-distance test.

Three-file syntax passes:

```sh
env PYTHONPYCACHEPREFIX=/tmp/qsearch-review-pycache /opt/anaconda3/bin/python -m py_compile locator.py test_locator.py replay.py
```

`/opt/anaconda3/bin/python -B replay.py --write` generates20 checked native
decodes, retains messages, error supports/values, recovered words and
locators, and hashes the actual construction dependencies. The decoder
itself receives only B and the received word. Higher-e entries are exact
rational analytic bounds, not generated inputs or measurements.

Final replay --write and --check pass. Receipt SHA256:
`0b863d6ed097f69a6d0746de1fe7cc78eb286751da747255d192ddda1729d713`.
The previous check failed only because the completed review newly entered
the provenance list; the structured comparison confirmed that only the
hashes field changed before the reviewed receipt was regenerated.

The separate literature review's `comparison_controls.py` was replayed:
16 acquired source hashes pass; three fixed prime/length controls verify
ordinary-DQI success=lambda*tau for all syndromes and the equal amplitudes
on verified full-support outputs. This is not an AG quantum execution.

Main `qsearch.py validate` returns validtrue and issues[]. `git diff --check`
passes. No root index.js exists; no UI changed and no node check is claimed.

## Scope And Handoff

The completed independent comparison review is in
../usd-novelty-review-2026-10-27/REVIEW.md. It checks the matrix-only locator,
truncated-source success and exact ideal conditional output law, and demotes
the family-level novelty claim. It does not independently certify the parent
implementation. The review document is complete; its agent was closed after
the document was read. The pair circuit's separate review is complete/closed.

No compiled reversible locator, truncated-source preparation circuit,
quantum sampler, larger native source, classical full-support solver,
registry promotion, CLI/UI wiring, commit/push or source migration.
The bundle is outside Git, under the local Developer research directory.
Repository checkpoint pointers are NOT a portable backup.
