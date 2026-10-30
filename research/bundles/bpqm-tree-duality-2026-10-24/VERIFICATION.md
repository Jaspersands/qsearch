# Verification: Binary Tree Duality

Date: 2026-10-24. External workspace only. LOCAL UNREVIEWED mathematics;
no independent review or formal proof-assistant verification of this bundle.

## Executed Checks

**500 tests passed** in 5.41s, warnings as errors, no skips: 36 new controls
and the preceding 464 external HDQI/Rees/cluster/central-rank controls.
Three Python files pass py_compile. `make_receipt.py --write` completed and
`make_receipt.py --output /tmp/qsearch-tree-duality-replay-2026-10-24.json`
reproduced receipt.json byte-for-byte. All six local source hashes recompute
correctly. All required owned command sessions completed.

The new controls include independent Bayes calculations, direct quantum parity
density matrices, exact native factor-tree Gibbs enumeration, directed rounding,
both independently iterated AB/BA streams, signed Nishimori moments, all-plus
boundary influence, validation failures and exact replay of twelve old rational
quantum fidelity bounds. Dense controls are small verification fixtures, not
candidate algorithms. The scalable path performs bounded-law arithmetic only.

## Live Mathematical Artifact

The (3,6), c=13/20 upper recursion first enters the sufficient classical
nonreconstruction basin at depth8. The depth12 q bound is below9/200, giving
the stated exact double-exponential tail for the UNROUNDED process. An all-plus
boundary independently retains magnetization >=99/100. No finite-graph sampler,
finite quantum block-error rate, all-classical hardness or speedup is admitted.

## Reproduction

From this directory:

```sh
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONPYCACHEPREFIX=/tmp/qsearch-tree-duality-pycache PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /opt/anaconda3/bin/python -m pytest -q -p no:cacheprovider -W error
env PYTHONPYCACHEPREFIX=/tmp/qsearch-tree-duality-pycache /opt/anaconda3/bin/python -m py_compile tree_duality.py test_tree_duality.py make_receipt.py
env PYTHONPYCACHEPREFIX=/tmp/qsearch-tree-duality-pycache /opt/anaconda3/bin/python make_receipt.py --write
env PYTHONPYCACHEPREFIX=/tmp/qsearch-tree-duality-pycache /opt/anaconda3/bin/python make_receipt.py --output /tmp/qsearch-tree-duality-replay-2026-10-24.json
cmp receipt.json /tmp/qsearch-tree-duality-replay-2026-10-24.json
```

The broad500-test command is the prior cluster-transfer VERIFICATION.md command
with bpqm-tree-duality-2026-10-24/test_tree_duality.py added, using this pass's
/tmp pycache prefix. All listed checks exited zero.

## Changes And Limits

New eight-file bundle: tree_duality.py, test_tree_duality.py,
reference_frontier.json, TREE_DUALITY.md, HANDOFF.md, make_receipt.py,
receipt.json and this record. The external checkpoint was updated. Prior frozen
bundles are unchanged; the new entry supersedes their next-step recommendation
where it assumed a reconstruction-barrier crossing from local tree success.

Migration remains needs_inspection. Desktop original, staging, main CLI,
registry, UI and Git were not modified. No main-repository tests, qsearch
validate, Node checks, commits or pushes ran. Integration is explicitly pending.
The one authorized Rees reviewer had already completed; no new reviewer ran.
