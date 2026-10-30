# Verification And Execution Boundary

2026-10-26. Isolated workspace:
/Users/jaspersands/Developer/qsearch-research-work.

## Files Added Or Changed

- REALIZATION.md: charged native prime-degree IsERP realization of the
  non-Bass scalar-order family; wrong-maximal-order output falsifier;
  source-advice audit and explicit limits.
- native_realization.py: supplied-order basis changes and legal query
  controls, reusing the existing source constructor and lattice routines.
- test_realization.py: 13 exact controls.
- replay_realization.py and receipt.json: reproducible execution scopes
  and dependency hashes.
- HANDOFF.md: Gemini integration and the next specific mathematical audit.
- This file and root RESEARCH_CHECKPOINT_2026-10-23.md.

The helper was initially called controls.py and renamed before final
verification to avoid a generic module-name collision. No previous source,
test, receipt or independent-review report was edited.

## Checks Run

- Initial suite: 10 PASS in1.11s; expanded suite: 12 PASS in1.46s.
- Final standalone: 13 PASS in1.69s, warnings as errors, no skips.
- Eleven-bundle regression before helper rename: 292 PASS in42.40s.
- FINAL eleven-bundle regression after rename: 292 PASS in43.13s,
  warnings as errors, no skips.
- Three final Python files pass py_compile.
- Final receipt --write --check, then separate --check: PASS.

Final regression command:

    /opt/anaconda3/bin/python -W error -m pytest -q native-nonbass-realization-2026-10-26 local-order-scope-2026-10-26 classical-symmetry-harvest-2026-10-26 additive-framed-source-2026-10-26 polarization-completion-probe-2026-10-25 native-suborder-preprocessing-2026-10-26 smooth-repolarization-2026-10-23 prime-square-flags-2026-10-23 source-field-audit-2026-10-23 elliptic-theta-input-2026-10-26 elliptic-field-normalization-2026-10-25

New receipt SHA256:
b0268625795064a05cc18559224d43422f5e8ce69876b696e805444012f1df7b

Preserved prior evidence:

- Local-order scope: d7b8b158fe7371ab352404e912e791c2cd3a54ff43dba4de59141cdb0c651f40
- Additive source: 57725d72e078ec35bd3460c66439e5475c427c450880a0aa2dd12194a1f67bb9
- Independent review: 471723b406440c0e73723a5d77e41dbc680cf10b88d9c8355de1e8b5fbeacc49

## What These Tests Prove And Do Not Prove

At q=3,5,17 the WRONG and correct supplied maximal orders both pass the
algebraic output gates. Only containment in the supplied target distinguishes
them. Actual native division was NOT executed. The source matrix is built
from suborder coordinates; its rational congruence is not itself a native
geometric-isomorphism certificate. All target orders in the tests are known.

The native IsERP realization and adjoint-construction argument are written
reductions conditional on the imported model algorithms, not backend runs.
No unknown isogeny/kernel/target order was recovered, no geometric label or
quantum source was executed, and no hardness, novelty or advantage established.
The alleged A7 encoding-only objection was checked against the primary PDF
and rejected; no error in that published canonicalization claim was found.

The main local checkout was rechecked and is still absent. This is focused
research validation, not whole-repository tests. No qsearch.py validate,
node --check, main registry/UI/CLI edit, commit or push was performed.
No new reviewer, live test session, or command session remains.
