# Verification And Handoff

2026-10-27. This is a theorem/architecture audit, not a receiver execution.

## Final Checks

117 selected tests PASS in 17.32s, including 40 new controls. Warnings were
errors, plugin autoload and pytest cache output were disabled:

```sh
env PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONPYCACHEPREFIX=/tmp/qsearch-review-pycache /opt/anaconda3/bin/python -m pytest -q -p no:cacheprovider -W error tests/test_rees_hsp_reduction.py tests/test_rees_complete_instrument.py tests/test_uniform_bch_rees.py tests/test_rees_cover_and_nontransverse_descent_audit.py tests/test_central_character_descent.py /Users/jaspersands/Developer/qsearch-research-work/rees-source-tree-2026-10-27/test_source_tree.py
```

Run that command from `/Users/jaspersands/Desktop/quantum algorithm search`.
The bundle alone needs python-flint and pytest. Python 3.13.5 at
`/opt/anaconda3/bin/python` was used. Three new Python files pass py_compile.
`python replay.py --write` and `python replay.py --check` both pass from
this directory. The replay is exact analytic accounting, not observed
quantum performance. Its four rows are:

| c | p | Per-stage label cap N and native cap B | Terminal-source upper bound | Originals needed on generic event |
|---|---|---|---|---|
| 8 | 2^127-1 | 1000 | 1.1499689237572871e-21 | 322560 |
| 16 | 2^127-1 | 1000 | 4.1069432068676165e-6 | 334764638208000 |
| 32 | 2^521-1 | 1000 | 1.1439551050802555e-98 | 8420186781878192965350976389120000000 |
| 32 | 2^521-1 | 1000000 | 1.7707693859518366e-5 | 8420186781878192965350976389120000000 |

The first test run failed an overly optimistic numeric threshold; the first
replay also failed Python's decimal-digit guard for large exact fractions.
Both were corrected explicitly, with regression controls retained. They
were not mathematical counterexamples to the architecture theorem.

Main `python qsearch.py validate`: valid=true, issues=[]. Full repository
suite NOT run. No JavaScript changed; no root index.js is being claimed
checked. No central registry, CLI, UI, candidate, commit, push or storage
migration changes were made.

Existing free_lazard_domain/make_rees_cover also reproduced the standard
class-three scope examples at p=5: r=3 gives homogeneous dimensions
(3,3,8), Rees grades (14,11,8); r=4 gives (4,6,20), Rees grades (30,26,20).
These are public algebra controls, not oracle or quantum runs and not proof
of the general no-codimension-one-abelian-subalgebra argument.

## Reviews And Files

Both independent reviewer documents were read in full; both agents are
closed. The prior-art reviewer did not review correctness. The source-tree
reviewer reconstructed the probability/ancestry argument but did not audit
the implementation. Parent accepted the conditional-cost and blockwise
qualifications and added the correlated-marginals control from the review.

- `source_tree.py`: exact rank bounds, actual filiform bracket, cost profile.
- `test_source_tree.py`: 40 controls, including adversarial access cases.
- `replay.py`, `receipt.json`: reproducible analytic certificate.
- `RESULT.md`: assumptions, proof, scope, falsifiers, review disposition.
- `RESEARCH_DECISION.md`: portfolio decision and exact next theorem question.
- `../rees-novelty-recheck-2026-10-27/REVIEW.md`: bounded primary-source review.
- `../rees-source-tree-review-2026-10-27/REVIEW.md`: independent adversarial review.

SHA256 of final receipt:
`880f1efc2e65f2176fd2607ca20553dd74607a57c37249142d0e6fe8c13baf4e`.

SHA256 of untouched source-tree review:
`cf5849e01fbc98769feea75d0166f1469f06f13937bf1a47cdd8b41428ac3873`.

SHA256 of untouched prior-art review:
`9a9e9d484d091c7a90e88b313d8774f050ca9dc7b9a82d0d63f2d45fe17e2f31`.

All these new bundles remain outside Git in the isolated Developer research
directory. The main AGENT_HANDOFF is a pointer, not a portable backup.
Gemini should not turn this into a generic HSP negative result or a new
accepted candidate. No routine CLI wiring is needed for this theorem audit.

Next theory task: investigate a genuinely adaptive/collective reduction of
arbitrary class-three HSP to known graph-state solvers, or another actual
theorem match. Existing fixed-chart and quotient-discard audits already
address simpler shortcuts. Do not repeat them or start scalar-solver
optimization as if it removed the destructive-source bottleneck.
