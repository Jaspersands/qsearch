# arXiv collision watch

Finds new arXiv papers that could kill, support or scoop a Q-Search track, and points
each one at the nearest retained negative, note or theorem module in the corpus index.

```bash
pip install "scikit-learn>=1.4"                   # all watch.py needs (numpy, scipy come with it)
python tools/arxiv_watch/watch.py                 # papers since the last run, with a 7-day overlap
python tools/arxiv_watch/watch.py --since 2026-09-18 --tracks dcp,dqi_opi
python tools/arxiv_watch/watch.py --relabel       # re-apply label rules to stored papers, no fetching
python tools/arxiv_watch/watch.py --replay-seeds  # classifier consistency check on the seed papers
python tools/arxiv_watch/watch.py --verdict 2610.06753 should-cite --reason "..." --action "..."
python tools/arxiv_watch/watch.py --action-done 2610.06753   # that verdict's action is carried out
```

Each track query is sorted newest first and paged (`--max` results per page, default 100)
until a page reaches back past the window start, at most `--max-pages` pages (default 10),
with arXiv's three-second pause between requests. If the page cap stops a query first, the
uncovered window is recorded under `gaps` in the JSON, printed as a warning and listed under
"Incomplete coverage" in the digest until a run of that track that was not cut short covers
it (`--since <start> --tracks <track>`). A `--since` that is not a `YYYY-MM-DD` date, a
`--max` or `--max-pages` below 1, or a track name not in `tracks.py` exits 2 before anything
is fetched.

The window starts seven days before each track's previous run (its `tracks_updated` entry;
14 days back on a track's first run). arXiv's `published` date is the v1 submission date,
and a paper can be listed several days after it is submitted (weekends, moderation holds),
so a one-day overlap lost papers. A `--tracks` run moves only the dates of the tracks it ran,
and a `--since` that starts after a track's usual window start leaves that track's date
alone, so its next run still fetches the days that run skipped. A collisions file written
before per-track dates has only `updated`; each track without a date of its own is taken to
have run then, and the next saving run records that date for it before moving `updated`.
Papers already stored are recognised by id and never re-reported or re-scored, with two
exceptions:

- A paper with a reviewed verdict (see [Verdicts](#verdicts)) gets the verdict copied onto
  its record and is listed in the digest's Reviewed table. A person's verdict moves it out of
  the possible-kill and possible-scoop sections; a judge's leaves it there, marked
  `judge: VERDICT`, until a person records one. Its machine label is unchanged.
- A stored possible kill or scoop with no verdict is relabelled `already-cited` once a note,
  record or literature file cites its id. The record keeps `relabelled_from` (the old label)
  and `relabelled_on`, and the run reports the count. `--relabel` drops both fields when it
  gives the paper any label but `already-cited`.

Outputs, rewritten only when a run finds a new paper, a coverage gap opens or closes, a
verdict is added, changed or withdrawn, a stored flag is relabelled, or another track's query
returns a stored paper (its `queried_by` list grows, as after a `--tracks` backfill), so a
quiet week leaves them byte-for-byte unchanged. A rewrite also moves `updated`, the
`tracks_updated` entry of every run track whose window started no later than usual, and the
digest's "Last updated" line to the run date. A verdict
for a paper the watch has not stored changes no record, so the run re-renders only the digest:

- `research/audits/arxiv_collisions.json`: every paper seen, with tracks, label, wording
  cues, the five nearest corpus records, the date first seen and, once reviewed, its
  verdict. Apart from the two exceptions above, repeated runs only add.
- `research/audits/ARXIV_WATCH.md`: the digest, newest first, with possible kills,
  possible scoops and related papers, then the Reviewed table. Every possible kill and scoop
  is listed; the Related section shows the newest 40 and says how many more the JSON holds.
- `research/audits/arxiv_verdicts.json`: the reviewed verdicts, keyed by arXiv id. Written
  by `--verdict` and by the judge import (`judge.py`); the source of truth for the Reviewed
  table.

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

## Verdicts

Labels are triage, verdicts are judgement. A verdict records what a reader decided after
reading the paper against the project:

```bash
python tools/arxiv_watch/watch.py --verdict 2609.40302 false-alarm \
    --reason '"SDP" matched a note on an LWE-style SDP decoder.' [--action "..."] [--by human]
```

This writes `research/audits/arxiv_verdicts.json`, copies the verdict onto the stored paper
and re-renders the digest. It fetches nothing and does not build the corpus index. The id
may carry a version, an `arXiv:` prefix or the abstract URL (`arXiv:2609.40302v2`); the
verdict is stored under the bare id the watch uses. An unknown verdict, or an id that is not
an arXiv id, exits 2; that includes a new-style id with the wrong number of digits for its
month (four after the dot up to 1412, five from 1501) or a month outside 01-12, so a typo
such as `2610.0675` is not recorded.

Keys written into the file by hand are read the same way, so `"arXiv:2609.40302v2"` is the
verdict for stored paper 2609.40302 and is rewritten bare on the next save. When two keys name
one paper, a person's entry outranks a judge's. Every mode of `watch.py` (but
`--replay-seeds`) and `judge.py` reads the file first and exits 2 without writing anything when
it is not JSON, is not `{"verdicts": {...}}`, an entry is not an object with one of the five
verdicts, a key is not an arXiv id, or two people's (or two judges') entries name one paper.
They do the same when `arxiv_collisions.json` cannot be read, and when `--root` has no
`research/` directory, so a mistyped `--root` never gets a fresh `research/audits/`.

| Verdict | Meaning |
|---|---|
| kill | The paper invalidates a project claim or retained result. |
| scoop | The paper publishes a result the project presents as new. |
| should-cite | No conflict, but a named document should cite the paper or narrow a sentence. |
| related-only | Shared topic; nothing to do. |
| false-alarm | The wording cue or the corpus match is spurious. |

Each entry holds `verdict`, `reason`, `action` (null when nothing is to be done), `by` and
`reviewed_on`. `action_done: true` marks an action already carried out; set it with
`watch.py --action-done ID` (exit 2 when the paper has no verdict or its verdict no action).
Re-recording a person's verdict without `--action` keeps the earlier action and its
`action_done`, and says so; a different `--action` starts not done, and `--action ""` clears
it. Without `--reason` the earlier reason is kept, and the output says so, only when the
verdict is unchanged; a changed verdict with a stored reason needs its own `--reason` (exit 2
otherwise). A person recording over a judge's verdict keeps neither the judge's reason nor its
action: `--reason` is needed, and the output names the judge's action so `--action` can adopt
it. The file is the
source of truth: every run copies its entries onto the stored records and drops a withdrawn
one. The digest's Reviewed table lists every entry, by verdict then id, with the paper's
machine label; an id the collisions file does not hold shows "not stored".

Seeding the file (the 22 verdicts of the 2026-10-21 review) changes every stored record it
names, so the first weekly run after a seed opens a pull request even when no new paper
arrives.

## Judging unreviewed flags

New possible kills and scoops arrive every week. `judge.py` hands the unreviewed ones (flagged,
no verdict) to in-session subagents, in the same export and import loop as `tools/audit/`:

```bash
python tools/arxiv_watch/judge.py --export DIR --batches 3
# one fresh subagent per batch reads DIR/INSTRUCTIONS.md and DIR/batch_NN.json, writes DIR/out/batch_NN.jsonl
python tools/arxiv_watch/judge.py --import DIR/out/*.jsonl --judge claude-subagent-2026-10-27
```

Each batch item has the paper's title, abstract, label, cues and tracks, and its nearest
Q-Search records with the first 600 characters of each. Batch files are UTF-8 with no `\u`
escapes, so the judge sees the characters the quote check compares. The judge writes one row
per paper:
`{"arxiv_id", "verdict", "reason", "quote", "quote_from", "action", "confidence"}`.

Import checks every row before it writes anything: a missing or unreadable file, a row that
is not a JSON object, an unknown verdict, an id that is missing or not stored, or a corpus
index that cannot be opened to check an excerpt quote stops it (exit 2) with nothing written.
The accepted rows are then merged into fresh copies of the verdicts and collisions files, one
write each, so a verdict or run recorded meanwhile is kept. A row is rejected when

- its quote is under six words (numbers count; symbols and TeX commands do not), or does not
  appear verbatim in the one text `quote_from` names: the abstract, or the excerpt of one of
  the paper's nearest records. Spacing, the case of ordinary Latin words (two or more letters,
  and the word "a"), sentence punctuation (`. , ; : ?`), quote marks and apostrophes, an em
  dash (`—`, `---`) or spaced en dash (` – `, ` -- `) between clauses, markdown's `**` and
  TeX's `$`, `\(`, `\)` and spacing commands (`\,`, `\quad`, `\qquad`, `\hspace{1em}` and the
  like) are ignored; every other dash, `--` and `−` read as `-`. The maths must match: signs,
  `/`, `!`, `#`, `%`, `^`, `_`, `×`, braces and brackets, Greek letters, TeX commands (`\Omega`
  is not `\omega`), spelled-out Greek capitals (`Omega` is not `omega`), the case of every
  other one-letter symbol (`O(n)` is not `o(n)`, `N` is not `n`), primes (`W'` is `W′`, never
  `W`; an `'` is a prime after a digit, a closing bracket, a one-letter symbol or a TeX command,
  and an apostrophe or quote mark otherwise), a decimal point (`.5` is not `5`, `2.9x` is
  `2.9 x`) and a ratio's colon (`1:2`). A superscript reads as its TeX exponent (`2ⁿ` is `2^n`,
  never `2n`). So a quote with `≥` for `≤`, `0.207` for `-0.207`, `n^{1/2}` for `n^{-1/2}`,
  `ω` for `Ω` or `o(n)` for `O(n)` fails. So does one that starts or ends inside a formula or
  a hyphenated word: just after an operator (a sign, `-`, `/`, `=`, `×`, `\cdot`, ...) or a
  prefix (`√`, `\sqrt`, `\log`, `#`, a decimal point), or just before an operator or a
  factorial, percent sign or prime that follows a number or symbol. A quote that runs from one
  text into another, or comes from a record the judge was not shown, is not evidence ("quote
  not found"). The texts are the ones the judge was shown: an output at `DIR/out/batch_NN.jsonl`
  is checked against the abstract and excerpts in `DIR/batch_NN.json`, so a note edited or a
  paper re-fetched after the export neither breaks a faithful quote nor admits one from the new
  text. A file elsewhere, or a paper missing from its batch, is checked against the stored
  abstract and today's excerpt. A batch file that is not a JSON object with a list of papers
  stops the import (exit 2);
- the paper already has a verdict recorded by anyone but a judge, including an entry written
  by hand without `by` ("human verdict exists").

Accepted rows go into `research/audits/arxiv_verdicts.json` with `by: "judge:NAME"`, the
quote, `quote_from` and `confidence` (clamped to 0..1; null when it is not a finite number,
is an integer too large for one, or is `true` or `false`). A later import may replace a judge's verdict, never a
human's. The stored records and the digest are then rewritten, and the Reviewed table shows
who decided. A judge verdict is one model's reading, so it never takes a flag out of the
possible-kill and possible-scoop sections: the paper stays there, marked `judge: VERDICT`,
until a person checks it (a `false-alarm` or `related-only` as much as a `kill` or `scoop`)
and records the outcome with `watch.py --verdict`.

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

- Unit tests (`tests/tools/test_arxiv_watch.py`, `tests/tools/test_arxiv_judge.py`) use a
  recorded arXiv API response and a fake client; nothing in the test suite touches the
  network.
- Verdict smoke run (2026-10-21, after seeding): `watch.py --relabel` on the branch checkout
  kept all 22 verdicts on their records; the possible-kill and possible-scoop sections were
  empty and the Reviewed table had 22 rows, none "not stored". The five flags the review calls
  already cited kept their labels there, because the notes that cite them were not committed
  yet. Four unflagged papers changed label or tracks under the branch's rules and index
  (2609.23818 and 2609.35511 to unrelated, 2609.31484 to already-cited, 2610.17711 lost
  hidden_shift). The relabelled outputs were not committed. A weekly run never recomputes
  labels: a simulated first weekly run with no new papers changed no label, only the 22
  verdict attachments and the run dates (`updated`, all 14 `tracks_updated` entries and the
  digest's "Last updated" line). The four changes need an explicit `watch.py --relabel`
  commit. Besides any new papers, the first pull request after seeding holds the 22 verdict
  attachments and the run dates. New papers are all but certain: that run fetches from a week
  before each track's last fetch (2026-10-11, and 2026-10-12 for number_theory), and the newest
  stored paper is from 2026-10-16. The workflow's PR body says what can change.
- Seed replay: all 52 seed papers whose tags name a track are placed on it. Nine
  patterns were added after the first replay missed them, so this is a consistency
  check on the seeds, not a held-out accuracy figure.
- First live run (2026-10-18, papers since 2026-09-18): 176 papers. Under the original
  rules: 11 possible kills, 5 possible scoops, 96 related, 8 already cited, 56 unrelated.
  After the rule change of 2026-10-19 (`--relabel`, offline): 4 possible kills, 11
  possible scoops, 96 related, 9 already cited, 56 unrelated. Eight of the eleven old
  kills were positive quantum papers tripped by "lower bound", "limitation" or a
  background "dequantized"; the ninth already-cited paper cites a versioned id.
- That run predates paging: each track query stopped at 50 results, and the number_theory
  query's 50 covered only 2026-10-13 to 2026-10-15. The backfill of 2026-10-19
  (`watch.py --since 2026-09-18 --tracks number_theory`, with paging) is committed: that query
  fetched 620 papers published 2026-09-18 to 2026-10-16, 542 of them new (3 possible kills, 4
  possible scoops, 54 related, 481 unrelated), and recorded no gap. It need not be run again.
  The file now holds 718 papers: 7 possible kills, 15 possible scoops, 150 related, 9 already
  cited, 537 unrelated. Its `tracks_updated` has number_theory at 2026-10-19 and the other 13
  tracks at 2026-10-18, their last fetch.
