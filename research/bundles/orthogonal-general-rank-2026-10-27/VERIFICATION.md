# Verification Ledger

2026-10-27. Working directory is this isolated bundle. Python is
`/opt/anaconda3/bin/python` (3.13.5). No packages installed, Git operations,
main-registry mutation, UI change or migration was performed.

## Executed Checks

```
env PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONPYCACHEPREFIX=/tmp/qsearch-review-pycache /opt/anaconda3/bin/python -m pytest -q -p no:cacheprovider -W error test_general_rank.py
```

40 new tests passed in 1.84 seconds.

```
env PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONPYCACHEPREFIX=/tmp/qsearch-review-pycache /opt/anaconda3/bin/python -m pytest -q -p no:cacheprovider -W error test_general_rank.py ../orthogonal-three-probe-2026-10-23/test_orthogonal_probe.py
```

75 selected tests passed in 4.07 seconds. This includes all 35 existing
maximal-three-probe controls, not the entire main repository test suite.

```
env PYTHONPYCACHEPREFIX=/tmp/qsearch-review-pycache /opt/anaconda3/bin/python -m py_compile general_rank.py controls.py test_general_rank.py replay.py
env PYTHONPYCACHEPREFIX=/tmp/qsearch-review-pycache /opt/anaconda3/bin/python replay.py --write
env PYTHONPYCACHEPREFIX=/tmp/qsearch-review-pycache /opt/anaconda3/bin/python replay.py --check
```

All passed. The receipt check freshly recomputes the deterministic controls.
From the main repository, `python qsearch.py validate` via the same Python
returned `valid: true`, `issues: []`, with 8 candidates, 796 experiments,
807 experiment results and 973 negative results. It validates the existing
registry, NOT the new theorem or an integration of this isolated bundle.
No root index.js exists and no JavaScript was changed; no Node check claimed.

## What The Controls Actually Establish

* Exact probe-kernel and complete-fiber comparisons over F_3 include all
  three positions of e, hidden ranks 1/2 as negative-range controls, and
  ranks 3/4 in ambient dimension eight.
* A concrete hidden rank-three subspace has bad probes producing the same
  wrong rank-four maximal extension. Reconstruction alone accepts its
  geometry; the containment certificate rejects the proposed answer.
* A smaller genuine subspace passes the certificate when contained in the
  true U. This is intentional evidence that the certificate is not an
  equality oracle and requires the kernel-rank provenance.
* Certificate tests span all nonempty coordinate singular subspaces under
  a nontrivial changed frame for the tested ranks, and test exact determinant
  one and orthogonality. Removing the central or cross tests gives explicit
  false positives. This is not an exhaustive general-field proof.
* Live opaque-label dense references over F_3, n=4, recover k=3 and k=4
  without passing k to the controller. Each takes two trials. They charge
  4384 and 3659 CLASSICAL oracle calls respectively, including tables and
  certification; table-only counts are 4374 and 3645.
* The n=8,k=5,p=2^127-1 receipt uses the supplied hidden subspace to CHECK
  the algebra. It does not simulate a Fourier learner or demonstrate
  learning at large primes. Other tests include p=2^61-1.
* The analytic n=64,p=2^127-1,error=2^-64 schedule has 113 trials,
  42714 Fourier instruments, and a 498444 original-query cap including
  certificates. These are proposed algorithm bounds, not measured runtime.

The receipt keeps quantum execution, natural application, literature novelty
and a general-rank classical lower bound false. The inherited maximal-only
budget's stale `independent_proof_review_completed` field was removed from
this new cost record. Review is recorded below with its scope, not promoted
to an unqualified Boolean about code, theorems and novelty together.

## Review Status

One independent reviewer reconstructed the written certificate, rank gate,
success bound, trace-annihilator recovery, resource/error ledger and
reflection comparison, and found no mathematical defect under the stated
contract. The parent read the complete report at
`../general-rank-orthogonal-review-2026-10-27/REVIEW.md`; reviewer closed.
No mathematical correction was requested. The reviewer also independently
ran exact small-field checks including F_9 invariant lines/planes; these
scratch checks are not retained regression tests and were not rerun by the
parent. They supplement the written proof, not replace it.

The reviewed RESULT.md SHA-256 is
`dac3c1c3e8e5c30d265b34cb9f47d5ba5b373b3bd66503077fc1157c7e440046`.
The report explicitly excludes code audit, formal verification, quantum
execution, novelty certification and natural-input advantage. Parent code
changes after review only remove stale inherited review metadata and add
its regression assertion; the theorem text is unchanged.

After that metadata change, all 75 selected tests passed again in 4.06
seconds; four-file syntax and receipt regeneration/check also passed.
Final receipt SHA-256:
`5984979148e883d6132d6173f73582a9b78af0b4b7005efce7a0cff10d490963`.
Independent review SHA-256:
`75f152859e5b232738a257daf4c6e4dffe5365db5494ee7cf05d9b531391db02`.
