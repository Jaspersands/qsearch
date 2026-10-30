# Verification: Correlated Source Shortcut

2026-10-27. These are finite algebra/density checks and symbolic arguments,
not execution of a scalable quantum receiver or evidence of a speedup.

## Executed Commands

From this directory:

```sh
env PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONPYCACHEPREFIX=/tmp/qsearch-review-pycache /opt/anaconda3/bin/python -m pytest -q -p no:cacheprovider -W error test_correlated_source.py ../rees-source-tree-2026-10-27/test_source_tree.py
env PYTHONPYCACHEPREFIX=/tmp/qsearch-review-pycache /opt/anaconda3/bin/python -m py_compile correlated_source.py test_correlated_source.py replay.py
/opt/anaconda3/bin/python replay.py --write --check
```

Final selected test run: **88 passed in 3.07s**, including 48 new tests and
40 previous source-tree tests. Three-file syntax check and deterministic
receipt regeneration/check pass. No earlier source-tree file was changed.

From `/Users/jaspersands/Desktop/quantum algorithm search`:

```sh
/opt/anaconda3/bin/python qsearch.py validate
```

Result: `valid: true`, `issues: []`, 8 candidates and 973 existing negative
records. No central registry record was added. The entire main suite and
JavaScript checks were not run; this pass did not change application code.

## Tested Scope

- Exact cyclotomic coefficients for all 486 p=3 and 6250 p=5 combinations
  of element, selected-grade label and hidden-line choice.
- Independently constructed coset densities and central projectors, sector
  normalization/positivity, and direct joint-source overlap sums.
- Right anti-representation ordering, opposite labels, equal-action identity,
  uniform-control dephasing and zero-label quotient coset states.
- Native two-evaluation Rees pullback, nonnormality and correct grade-one
  duplication of the original central coordinate.
- First-marginal twirl, one-copy recovery, and the independent reviewer's
  left-action escape on every p=3 label for both hidden lines.
- Integer isometry-compression matrices commute with right generators.
- Exact capped-probability bounds and invalid-parameter guards.

The large-prime row p=2^61-1, T=10^6 is purely analytic. Its rare-event bound
is 1000000/2305843009213693951, and the weak necessary source count for
two-thirds binary success is 768614336404564651. This is restricted to the
specified mixed source and observable algebra. The binary promise itself
has a two-query classical test; no unrestricted hardness is asserted.

## Independent Review

One focused independent mathematical reviewer examined the source, action
ordering, full-grade example, conditional law and joint/adaptive protocol
bound. The review is in the sibling
`../rees-correlated-source-review-2026-10-27/REVIEW.md`.
The parent read the review and final addendum in full and incorporated its
four scope qualifications and explicit left-action counter-control. The
reviewer also independently verified both directions of the new weak-Fourier
corollary and its joint/adaptive scope. No further mathematical correction
was required. The reviewer is closed. The review does not audit the
implementation or certify novelty.

Frozen receipt SHA256:
`9c39a653b1ad15d22349840fe3ced2e877e691435a54ed627e639d72d921e4d9`.

Completed review SHA256:
`21dc599332972488b02c3b316782a2b88d816a8f8557f2aefefb43a2c01dcd21`.

No commit, push, CLI/UI change, dependency installation, or storage repair.
The new executable bundle and review remain outside Git. Handoff pointers
do not back them up. Existing dirty changes are preserved.
