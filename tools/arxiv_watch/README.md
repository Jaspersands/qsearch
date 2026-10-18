# arXiv collision watch

Finds new arXiv papers that could kill, support or scoop a Q-Search track, and points
each one at the nearest retained negative, note or theorem module in the corpus index.

```bash
pip install -r requirements-tools.txt
python tools/arxiv_watch/watch.py                 # papers since the last run (default: 14 days)
python tools/arxiv_watch/watch.py --since 2026-09-18 --tracks dcp,dqi_opi
python tools/arxiv_watch/watch.py --relabel       # re-apply label rules to stored papers, no fetching
python tools/arxiv_watch/watch.py --replay-seeds  # classifier consistency check on the seed papers
```

Outputs, both regenerated on every run:

- `research/audits/arxiv_collisions.json`: every paper seen, with tracks, label, wording
  cues, the five nearest corpus records and the date first seen. Papers already present
  are never re-scored, so repeated runs only add.
- `research/audits/ARXIV_WATCH.md`: the digest, newest first, with possible kills,
  possible scoops and related papers.

## Tracks and labels

`tracks.py` defines 14 tracks. Each has an arXiv query (restricted to quant-ph, cs.CC,
cs.DS, cs.CR, cs.IT, math.RT and math.NT), text patterns that place a paper on the track,
and the literature seed tags that belong to it. Ten are core (DCP, hidden shift,
nonabelian HSP, representation theory, code equivalence, DQI/OPI, BPQM/Gibbs, lattices,
number theory, state discrimination); four are peripheral (dequantization, QSVT,
algorithm discovery, query complexity and sparse Fourier).

| Label | Rule |
|---|---|
| already-cited | The arXiv id already appears in a note, record or literature file. |
| possible-kill | Core track, mentions quantum, and wording like "dequantize", "efficient classical", "no-go", "lower bound", "refute". |
| possible-scoop | Core track, mentions quantum, and wording like "exponential speedup", "polynomial-time quantum algorithm", "quantum advantage". |
| related | On a track but neither of the above, or only on peripheral tracks. |
| unrelated | Fetched by a query but matches no track pattern. |

Labels are triage, not judgement. A "possible kill" means "read this before the next
pass on that track".

## Scheduling

`.github/workflows/arxiv_watch.yml` runs every Monday and on demand. When the digest
changes it pushes a branch and opens a pull request; it never commits to `main`. The
repository setting *Allow GitHub Actions to create and approve pull requests* must be
on for the PR step to succeed.

## Checks

- Unit tests (`tests/tools/test_arxiv_watch.py`) use a recorded arXiv API response and
  a fake client; nothing in the test suite touches the network.
- Seed replay: all 52 seed papers whose tags name a track are placed on it. Nine
  patterns were added after the first replay missed them, so this is a consistency
  check on the seeds, not a held-out accuracy figure.
- First live run (2026-10-18, papers since 2026-09-18): 176 papers, of which 11 possible
  kills, 5 possible scoops, 96 related, 8 already cited and 56 unrelated.
