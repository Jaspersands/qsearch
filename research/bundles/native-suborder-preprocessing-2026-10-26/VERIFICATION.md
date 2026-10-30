# Verification, 2026-10-26

Status: PROGRESS on the written native-input reduction and finite interfaces,
not an executed quantum algorithm. Workspace:
/Users/jaspersands/Developer/qsearch-research-work.

Implemented native_preprocessing.py, test_native_preprocessing.py and
replay_native_preprocessing.py. Added PREPROCESSING.md, HANDOFF.md,
sources.json, three retained primary PDFs and receipt.json. Added a separate
Finding 1 follow-up without altering the independent review. Updated the
root research checkpoint. No main CLI, registry, UI, source/staging or Git
edits, commit or push. This research directory is not a Git checkout.

Executed using /opt/anaconda3/bin/python:

- Initial new tests: 23 passed in 1.95s.
- After the CM/Frobenius self-review repair: 26 passed in 2.31s.
- Initial seven-bundle focused regression: 218 passed in 13.51s.
- FINAL seven-bundle focused regression: 221 passed in 14.45s, warnings as
  errors, no skips. Includes this bundle, elliptic-theta-input,
  elliptic-field-normalization, source-field-audit, source-algebra-splitting,
  double-level-source and suborder-transcript.
- py_compile: all three new Python files passed after final code edits.
- replay_native_preprocessing.py --write --check: passed.
- Separate replay_native_preprocessing.py --check: passed identically.
- All three downloaded PDFs opened successfully and their hashes match
  sources.json. The receipt independently verifies those hashes.

Commands, relative to the workspace:

```sh
/opt/anaconda3/bin/python -W error -m pytest -q native-suborder-preprocessing-2026-10-26 elliptic-theta-input-2026-10-26 elliptic-field-normalization-2026-10-25 source-field-audit-2026-10-23 source-algebra-splitting-2026-10-25 double-level-source-2026-10-25 suborder-transcript-2026-10-25
/opt/anaconda3/bin/python -m py_compile native-suborder-preprocessing-2026-10-26/native_preprocessing.py native-suborder-preprocessing-2026-10-26/test_native_preprocessing.py native-suborder-preprocessing-2026-10-26/replay_native_preprocessing.py
/opt/anaconda3/bin/python native-suborder-preprocessing-2026-10-26/replay_native_preprocessing.py --check
```

Receipt SHA256:

    608e29bf0ba88186ca15bf46ece5f23bd09c37edddc4f9f85e87cbf0da6756c1

Original independent REVIEW.md SHA256, unchanged:

    471723b406440c0e73723a5d77e41dbc680cf10b88d9c8355de1e8b5fbeacc49

The live receipt distinguishes two supplied arithmetic suborder/tensor
controls from three actual reference curves over F_49,F_529,F_961. Each
native curve tests 64 half points above 16 inputs. Three abstract quaternion
controls verify the discriminant formula used to bound noncommutation; they
do not prove the general CM construction was executed.

General CM construction and source saturation, rational tensor splitting,
native target preprocessing, a geometric canonical label and a coherent
quantum source were NOT run. General field-tower integration remains absent.
The main repository's full tests, qsearch validation and Node checks were
not run or claimed; no main files were changed. All command sessions finished.
