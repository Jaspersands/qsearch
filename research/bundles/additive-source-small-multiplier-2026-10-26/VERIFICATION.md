# Verification: Additive Source Small Multiplier

2026-10-26. Workspace /Users/jaspersands/Developer/qsearch-research-work.
All evidence below is exact supplied-order arithmetic. Native geometry,
unknown-order recovery and quantum execution remain unimplemented here.
The new theorem and comparator have not had independent review.

## Completed Commands

    /opt/anaconda3/bin/python -W error -m pytest -q additive-source-small-multiplier-2026-10-26

29 passed in 12.01s, warnings as errors, no skips.

    /opt/anaconda3/bin/python -W error -m pytest -q additive-source-small-multiplier-2026-10-26 query-quadratic-baseline-2026-10-26 active-coset-density-2026-10-26 full-suborder-impact-audit-2026-10-26 additive-framed-source-2026-10-26 classical-symmetry-harvest-2026-10-26 nonfree-factor-bound-2026-10-26

169 passed in 32.63s, warnings as errors, no skips. This is a seven-bundle
focused regression, not an all-tests claim for the unavailable main repo.

    /opt/anaconda3/bin/python -m py_compile additive-source-small-multiplier-2026-10-26/small_multiplier.py additive-source-small-multiplier-2026-10-26/test_small_multiplier.py
    /opt/anaconda3/bin/python additive-framed-source-2026-10-26/replay_additive_source.py --check
    /opt/anaconda3/bin/python classical-symmetry-harvest-2026-10-26/replay_harvest.py --check

All exited 0. All tool command sessions completed. The two preserved
receipts were checked without rewriting their historical contents.

## Checked Controls

- Reordered block identities, integral inverse and isogeny multiplier at
  n=2,3,5 with zero, scalar and general quaternion queries.
- Both directions of the rational recovery identity, exact degree sums,
  and quadratic-field escape equivalence for supplied automorphisms.
- A g=128 automorphism mixing copies with the SAME n^4 degree bound.
- Forty-digit scalar shifts and multiples do not change the bound when a
  fixed primitive orientation of the same field is used.
- Commutator norm/discriminant identity and ramified-prime divisibility;
  the p=7 equality example genuinely has a nonzero commutator.
- Pell index17 erasure for all16 group generators and three nonzero
  translation classes, with the exact identity proving the entire-group
  result. Useful original symmetries can have all pulled entries in R.
- Noncommutation alone is insufficient: a pulled map can leave the query
  field while already belonging to R.
- Fractional H-unitaries, nonisometries, tampered multiplier data, wrong
  orientations and invalid numerical inputs are rejected.

Native provenance cannot be established by these controls. The code marks
native model construction, extraction and orientation authentication false.
The no-growth conclusion additionally requires the actual native quadratic
saturation gate to have completed without growing R. Failure of the bound
is explicitly NO CONCLUSION, not an accepted positive candidate.

## SHA-256

    1b666c5bb5ad71735bc20e4387c9c7c3f321da48fe2ed8db5f51291da1135e1f SMALL_MULTIPLIER.md
    346ab89d26b56fac31460c5563d6e930f856323b2ab69cd079729be0aa02b39d small_multiplier.py
    36682fc65cc75217e260f3acbc7efe39ac7ec90cb64515fdf3064bdf84d6ab9d test_small_multiplier.py

Preserved predecessor artifacts:

    a15870b074c5ae2765bee5bb36c891b42c499d2de69ad02d666a3f95acbc3d15 query-quadratic-baseline-2026-10-26/QUADRATIC_BASELINE.md
    2c4b7ea6b15d6783dd9da827dd4b66bce33aeab1036bc9f9aa90f24d78fad9cc additive-source-independent-review-2026-10-26/REVIEW.md
    60fdb0114a04c292ccbfb459938a29f6d083586e550347f70e5eec7d80ad06d6 active-coset-density-2026-10-26/ACTIVE_COSETS.md

The approved prior review is not an independent review of this extension.
No new reviewer was used. The intended main local checkout was rechecked
and remains absent. No original/staging checkout, qsearch.py, main tests,
central registry, index.js, UI, Git commit or push was modified.
