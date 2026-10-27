# Local Review-Package Verification

27 October 2026. This ledger concerns source reconciliation and selected
controls, not a new theorem, peer review, novelty decision or quantum run.

## Source Reconciliation

The repository's `rees_hsp_review.tex` now incorporates exactly the F1
actual-class normalization paragraph from the isolated corrected revision:

`/Users/jaspersands/Developer/qsearch-research-work/rees-independent-review-2026-10-23/rees_hsp_review_revised.tex`.

A direct diff after reconciliation shows only two remaining differences:
the author status says `not peer-reviewed` instead of `not independently
reviewed`, and the date is 27 rather than 22 October. The mathematical text
is otherwise identical. This preserves the distinction between an automated
adversarial review and human specialist/peer validation.

The two files in `review_evidence/` were copied without editing. Both `cmp`
checks against their isolated originals exited zero. Their historical
absolute file links and snapshot hashes are intentionally preserved, not
presented as portable current-file references.

SHA-256 fingerprints:

```
dc92967068ef507c48fc5dc9ea8d9e5685d13219920b51df3fc01ba6ad4bb31f  rees_hsp_review.tex
74a46bd40517fc648c70c48b696b28fdeccd4b67576a7f7133338e6ccb056f24  review_evidence/2026-10-23-correctness-review.md
9a9e9d484d091c7a90e88b313d8774f050ca9dc7b9a82d0d63f2d45fe17e2f31  review_evidence/2026-10-27-prior-art-scope.md
```

The brief and outreach draft introduce no new theorem statement beyond the
scopes already in those sources. No recipient was selected, message sent,
paper submitted or author contacted. Saving this package in the user's
existing Git repository is distinct from expert outreach or submission.

## Executed Checks

From the repository root:

```
env PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONPYCACHEPREFIX=/tmp/qsearch-review-pycache /opt/anaconda3/bin/python -m pytest -q -p no:cacheprovider -W error tests/test_rees_hsp_reduction.py tests/test_uniform_bch_rees.py tests/test_rees_complete_instrument.py tests/test_rees_copy_only_outer.py
```

**76 selected tests passed in 9.14 seconds**, including two new
parameterized regressions for F1 at p=5 and p=2^127-1. The compiler computes
the Heisenberg profile (3,1), uses two original calls per lifted source,
and gives six original inputs per scalar-line terminal source. The loose
valid upper bound p-1 does not enter that computed schedule. Production
code already behaved this way; the correction is to the proof exposition.

```
env PYTHONPYCACHEPREFIX=/tmp/qsearch-review-pycache /opt/anaconda3/bin/python -m py_compile tests/test_rees_hsp_reduction.py theorems/rees_hsp_reduction.py theorems/uniform_bch_rees.py
env PYTHONPYCACHEPREFIX=/tmp/qsearch-review-pycache /opt/anaconda3/bin/python qsearch.py validate
git diff --check
```

All passed. Registry validation returned `valid: true`, `issues: []`;
the counts remain 8 candidates, 796 experiments, 807 experiment results,
973 negative results. No claim or registry status was promoted.

The desktop LaTeX compiler reported `kind: success` for the saved
`rees_hsp_review.tex`. This confirms compilation, not mathematical validity.
It does not export a deliverable PDF, so this pass does not claim that a
PDF attachment exists. No UI or JavaScript was changed; no Node check was
needed or claimed. The entire repository suite was not run.

## Remaining Decision

The main open scientific questions are correctness under specialist
reconstruction, exact prior-art subsumption, and meaningful natural-input
usefulness. None follows from the checks above. The user's request to see
the proposed email did not authorize sending it; the next contact step
requires an explicit instruction and an identified recipient.
