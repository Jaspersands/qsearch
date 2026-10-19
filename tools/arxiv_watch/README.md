# arXiv collision watch

Finds new arXiv papers that could kill, support or scoop a Q-Search track, and points
each one at the nearest retained negative, note or theorem module in the corpus index.

```bash
pip install "scikit-learn>=1.4"                   # all watch.py needs (numpy, scipy come with it)
python tools/arxiv_watch/watch.py                 # papers since the last run, with a 7-day overlap
python tools/arxiv_watch/watch.py --since 2026-09-18 --tracks dcp,dqi_opi
python tools/arxiv_watch/watch.py --relabel       # re-apply label rules to stored papers, no fetching
python tools/arxiv_watch/watch.py --replay-seeds  # classifier consistency check on the seed papers
```

Each track query is sorted newest first and paged (`--max` results per page, default 100)
until a page reaches back past the window start, at most `--max-pages` pages (default 10),
with arXiv's three-second pause between requests. If the page cap stops a query first, the
uncovered window is recorded under `gaps` in the JSON, printed as a warning and listed under
"Incomplete coverage" in the digest until a run of that track that was not cut short covers
it (`--since <start> --tracks <track>`).

The window starts seven days before each track's previous run. arXiv's `published` date is
the v1 submission date, and a paper can be listed several days after it is submitted
(weekends, moderation holds), so a one-day overlap lost papers. Papers already stored are
recognised by id and never re-labelled or re-reported.

Outputs, rewritten only when a run finds a new paper (or a coverage gap opens or closes),
so a quiet week leaves them byte-for-byte unchanged:

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
| already-cited | The arXiv id already appears in a note, record or literature file, with or without a version suffix (`2609.35656v1`, `arXiv:2609.40250v2`). |
| possible-kill | Core track, mentions quantum, and a classical-algorithm or negative-result framing: a classical algorithm in the title, "we give an efficient classical algorithm", "we dequantize", "rule out quantum advantage", "can exceed ... by at most", "any quantum algorithm requires". |
| possible-scoop | Core track, mentions quantum, and positive quantum framing: "we give a quantum algorithm", "efficient quantum algorithm", an exponential or provable quantum advantage claimed by the authors. |
| related | On a track but neither of the above, or only on peripheral tracks. |
| unrelated | Fetched by a query but matches no track pattern. |

Precedence: a kill framed in the title, then a scoop framed in the title, then any positive
quantum framing in the abstract, then a kill cue in the abstract. A sentence that states a
negative result contributes no scoop cue. Bare words such as "lower bound", "limitation"
or a "no-go" attributed to prior work are not cues: positive papers use them for their own
optimality proofs. A paper with both framings (say an efficient classical algorithm in one
regime and a quantum algorithm in another) is labelled a scoop; its cue column shows both.

Labels are triage, not judgement. A "possible kill" means "read this before the next
pass on that track".

## Scheduling

`.github/workflows/arxiv_watch.yml` runs every Monday and on demand. When the digest
changes it pushes a branch named `arxiv-watch/<date>-<run id>-<attempt>` and opens a pull
request; it never commits to `main`. The checkout does not keep the write token
(`persist-credentials: false`), the job installs only scikit-learn, and only the push step
authenticates. The repository setting *Allow GitHub Actions to create and approve pull
requests* must be on for the PR step to succeed.

A pull request opened with the workflow's `GITHUB_TOKEN` does not trigger other workflows,
so `tools.yml` does not run on it. Push a commit to the branch, or close and reopen the PR,
to get CI.

## Checks

- Unit tests (`tests/tools/test_arxiv_watch.py`) use a recorded arXiv API response and
  a fake client; nothing in the test suite touches the network.
- Seed replay: all 52 seed papers whose tags name a track are placed on it. Nine
  patterns were added after the first replay missed them, so this is a consistency
  check on the seeds, not a held-out accuracy figure.
- First live run (2026-10-18, papers since 2026-09-18): 176 papers. Under the original
  rules: 11 possible kills, 5 possible scoops, 96 related, 8 already cited, 56 unrelated.
  After the rule change of 2026-10-19 (`--relabel`, offline): 4 possible kills, 11
  possible scoops, 96 related, 9 already cited, 56 unrelated. Eight of the eleven old
  kills were positive quantum papers tripped by "lower bound", "limitation" or a
  background "dequantized"; the ninth already-cited paper cites a versioned id.
- That run predates paging: each track query stopped at 50 results. The number_theory
  query returned exactly 50 papers covering only 2026-10-13 to 2026-10-15, so its papers
  from 2026-09-18 to 2026-10-12 were never fetched. The JSON has no gap entry for it (gaps
  are recorded only by a fetching run); backfill with
  `watch.py --since 2026-09-18 --tracks number_theory`.
