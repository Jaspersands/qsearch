# Verification: Dilation-Averaged Source

2026-10-25. Updated after the independent AI review and local F1 correction.
All commands below completed. No quantum execution, hardware experiment,
full-repository validation or formal proof-assistant verification is claimed.
REVIEW.md and REVIEW_RESPONSE.md delimit the independent review's scope.
The same reviewer's CORRECTION_CHECK.md independently accepts the F1
repair and records its checked hashes. It did not rerun tests or certify
an implementation. The parent checks below are separate evidence.

## Tests

From `/Users/jaspersands/Developer/qsearch-research-work`:

```sh
/opt/anaconda3/bin/python -B -W error -m pytest -q -p no:cacheprovider \
  rees-dilation-average-2026-10-25 \
  rees-uniform-measurement-2026-10-24 \
  rees-spectral-mixture-2026-10-24
```

Current result: **108 passed in 14.54s**. This comprises 54 current-bundle
tests and 54 related tests. Warnings were errors. The previous 99-test
receipt is preserved in reviewed_snapshot/. The nine added tests cover the
shared-scale source falsifier and query/gate accounting after review.

Coverage includes symbolic Jacobian and inverse identities, both inverse
branches, complete regular-fiber inversion at p=5, regular censuses at
p=5,7,11, exact 127-bit-prime controls without enumeration, representation
product phases, nonsymmetric singular-value guards, zero-moment phase
erasure, class-three quotient maps and a class-four exclusion.

The final direct-proof controls check the cubic kernel identity symbolically
and ALL nonlinear irreps at p=5,7,11,13, including both exceptional square-map
branches. These are controls of the written proof, not a finite-size claim
of an asymptotic speedup or a new hard input family.

## Syntax And Receipt

Compiled the text of all six current Python files with Python's `compile`:
**6 syntax checks PASS**, no cache files. Historical .py.txt files are not
collected by pytest and were instead checked against their original hashes.

From this bundle:

```sh
/opt/anaconda3/bin/python -B replay.py write
/opt/anaconda3/bin/python -B replay.py check
```

Both PASS. Final `receipt.json` SHA256:

```text
aa9a0f74210c61edd88b116c165e29d957ccfb14a74be6050ee8579900fca687
```

The receipt hashes two mathematical notes and five parent Python sources.
It does not certify the reviewer's code; those checks are recorded below.
Its spectra are
rounded numerical controls; its large-prime budget is conditional, NOT a
validated receiver plan. For the diagnostic parameters delta=1/2, 1024
address bits, 100 receiver leaves, error=1/100 and design size24, it charges
159,744,000 raw pure copies and at most that many coherent SELECT(U) calls.
It explicitly does not certify a gate count. The 100-leaf input is not
certified sufficient for any actual Rees instance. Polynomial asymptotics
do not mean practical.

All four proof/code hashes in reviewed_snapshot/ match the old receipt,
whose SHA256 remains
9a6f31f65bafa3d9a4fc90e5917245819b2320cfff422f9b9727890c9b96a590.

## Independent Controls

The parent reran `/opt/anaconda3/bin/python -B -W error independent_controls.py`:
PASS. Parsed output matches ALL saved scientific fields in
independent_controls_results.json. The saved file also has command/exit-code
metadata, checked separately. An initial whole-object comparison failed
solely because stdout omits those two metadata fields; no scientific output
differed and no reviewer files were edited to obtain the match.

These checks independently cover the word/Jacobian and inverse identities,
cubic completion, 25 exact nonnormal source address pairs at p=131, the
wrong-orientation falsifier and the shared-scale falsifier. They are not
an implemented receiver or finite evidence of an asymptotic speedup.

## Scope And Workspace

Only this isolated bundle and the parent research checkpoint were changed.
The intended `/Users/jaspersands/Developer/quantum algorithm search`
destination remained absent on the live check. No main checkout, staging,
Git, central registry, CLI, UI or migration files changed. No commit/push.
Repository-wide `qsearch.py validate` and `node --check index.js` were NOT
run: those files were not changed and integration remains deferred.

No test or research process was left running. The research goal remains
active; the next scientific gate is a useful native application, not another
parameter extension. The SAME reviewer completed a separate check of this
deduction; neither that review nor these controls certify the whole program.
