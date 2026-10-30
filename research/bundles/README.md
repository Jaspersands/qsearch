# Research Bundles

These are working directories from 2026-10-22 to 2026-10-27, copied on
2026-10-30 from `~/Developer/qsearch-research-work/`. They were made while
iCloud eviction made the Desktop checkout unreliable. Several handoff
entries cite them as the only copy of a result, so they now live in Git.

Path mapping: a handoff path
`/Users/jaspersands/Developer/qsearch-research-work/<bundle>/<file>` is
`research/bundles/<bundle>/<file>` here.

Only the bundles' own text was copied: notes, code, JSON receipts, Lean and
TeX sources. These were left out:

- Lean build caches (`.lake/`, 6.9 GB) and the vendored Mathlib copy
- virtual environments and pip caches
- downloaded third-party papers (PDF, HTML, extracted text under `sources/`)
- page renders under `tmp/`

The originals are still in `~/Developer/qsearch-research-work/`.

The bundles' own `test_*.py` files are records of what each bundle checked.
They are not part of the repository suite; `conftest.py` here keeps pytest
from collecting them.
