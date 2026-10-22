# Corpus index: "has this been tried?"

One searchable index over everything Q-Search has written down: the negative-result
registry, dequantization checks, experiments and results, research notes, the agent
handoff journals, theorem modules, literature records and hypothesis contracts. Use it
before proposing a direction, so a new pass starts from the nearest retained negative
instead of rediscovering it.

```bash
pip install -r requirements-tools.txt
python tools/corpus/cli.py been-tried "measure each coset packet with its own Helstrom test and multiply"
```

`been-tried` prints five groups (killed before, dequantization checks, notes and handoff,
code and experiments, literature), each with `file:line` locations, the record's status
and, for negatives, the recorded reason it failed. A close match is a lead to read, not a
verdict on the idea.

## Commands

| Command | What it does |
|---|---|
| `been-tried IDEA [-k 5]` | Closest documents per group. |
| `search QUERY [--kinds negative,note] [--tags DCP]` | One ranked list, optionally filtered. |
| `similar DOC_ID` | Documents most like one result. |
| `get DOC_ID` | Full text and metadata as JSON. |
| `build [--full] [--dense]` | Build or update the index; `--dense` adds local sentence embeddings. |
| `heldout CASES.json [--min N]` | Retrieval check: each `{id, query}` must find its record in the top k. |
| `near-duplicates [--threshold 0.9] [--per-family N] [--limit 200] [--out FILE.json]` | Pairs of negatives with a high TF-IDF cosine (see Duplicates). |
| `check-new --text CLAIM \| --file RECORD.json [--threshold 0.6] [--allow ID]` | Exit 2 when a draft negative is close to a retained or quarantined one, 1 when the draft cannot be read or has no words. |
| `baselines IDEA [-k 5]` | Classical baselines the idea should be compared against (see Baselines). |

Every command except `build` first refreshes the index incrementally: it stats about
2,100 source files and re-parses only those whose size, mtime and content hash changed.
When nothing changed the refresh only reads (no write lock) and costs 0.05 to 0.15 s of
CPU. Every command but `build` takes `--no-refresh` to skip it. `--json` prints
machine-readable output from `search`, `been-tried`, `similar`, `heldout`, `near-duplicates`,
`check-new` and `baselines` (`get` always prints JSON). `--dense` adds the embedding ranker to
`search`, `been-tried`, `similar` and `heldout` (`build --dense` computes the embeddings); the
other commands reject it as an unknown flag with exit 2, which for `check-new` is also the
duplicate status, so a script should read `duplicate` from `--json` rather than trust the exit
code alone. `--root PATH` (or `QSEARCH_ROOT`), given before the command, indexes another
checkout. A root that is not a directory
with a `research/` directory is an error (exit 1) before anything is written, and so is a
checkout with nothing to index; the MCP server refuses to start on either.

A file or registry record that cannot be parsed is never silent. Every command prints the
problem on stderr and JSON output carries `index_issues`. When the problem is in
`research/registry/` (say a half-written `negative_results.json`), `index_incomplete` is
true, `been-tried` prints INDEX INCOMPLETE and exits with status 2: an empty "Killed
before" group then means the registry could not be read, not that the idea is new.

## For the research agents (MCP)

`tools/corpus/mcp_server.py` is a stdio MCP server exposing `been_tried`,
`search_corpus`, `get_doc`, `screen_dqi_candidate` (the DQI soundness screen, see
`tools/dqi_screen/README.md`), `classical_baselines` (the `baselines` command, below) and
`check_duplicate_negative` (the `check-new` check, below).
It keeps the index warm and refreshes it at most every 30
seconds, except `check_duplicate_negative`, which refreshes before every check so a record
another agent filed a moment ago is compared. With the default `--dense auto` it adds the embedding ranker only while every
document has a vector (after `build --dense`); documents added since then switch it back
to lexical ranking until the next `build --dense`, because a ranker that cannot see the
newest records would push them down. `--dense on` embeds new documents at each refresh
instead. Results carry `index_incomplete` and `index_issues` as above. Point each agent's
own configuration at it; nothing in the repository needs to change.

Use the Python that has `requirements-tools.txt` installed (here `/opt/anaconda3/bin/python3`).

Codex (`~/.codex/config.toml`):

```toml
[mcp_servers.qsearch_corpus]
command = "/opt/anaconda3/bin/python3"
args = ["/Users/jaspersands/Desktop/quantum algorithm search/tools/corpus/mcp_server.py"]
```

Gemini CLI (`~/.gemini/settings.json`):

```json
{"mcpServers": {"qsearch_corpus": {
  "command": "/opt/anaconda3/bin/python3",
  "args": ["/Users/jaspersands/Desktop/quantum algorithm search/tools/corpus/mcp_server.py"]
}}}
```

Claude Code:

```bash
claude mcp add qsearch-corpus -- /opt/anaconda3/bin/python3 "/Users/jaspersands/Desktop/quantum algorithm search/tools/corpus/mcp_server.py"
```

Suggested line for each agent's standing prompt: *Before proposing or extending a
direction, call `been_tried` with a one-paragraph description of the idea, read the
nearest retained negatives, and say how the new proposal escapes them.*

## How it works

- **Sources** (`sources/`): registry records become one document each, titled by their
  claim (templated dequantization claims are titled by their target instead). Notes are
  chunked at `## ` headings and re-split above 400 words, with a status read from the
  first eight lines (`review-pending`, `superseded`, `quarantined`, ...). Handoff
  sections keep their rank (0 = newest) and get ids numbered from the oldest, so ids
  survive new sections being added on top. Ids are unique within a file even when a
  repeated heading, a split section and a heading such as "Results 2" share a slug.
  Theorem modules are summarized from their docstrings with `ast`, never imported. A
  registry record of an unexpected shape is skipped and counted as an issue; a file that
  fails to parse for any reason (one committed hypothesis contract currently has an
  invalid JSON escape) is indexed as raw text with status `unparseable` and an issue.
- **Storage** (`store.py`): `research/corpus_index/corpus.sqlite` (WAL) holds file
  states, documents, an FTS5 table, dense vectors keyed by content hash and the parse
  issues. Files are parsed before the write lock is taken; changes are applied in one
  transaction that rolls back on any exception, so a crash never leaves the lock held.
  A changed file is diffed against its stored documents by content hash: unchanged
  documents keep their row, so editing one record of the 2.5 MB negative registry changes
  one document, not all 1,191. The directory ignores itself in git.
- **Ranking** (`ranking.py`): SQLite FTS5 BM25 with the Porter stemmer, plus word
  unigram/bigram TF-IDF cosine, fused by reciprocal rank. Optional third ranker: local
  `sentence-transformers/all-MiniLM-L6-v2` embeddings (offline once cached). TF-IDF is
  patched with the changed documents and refit when more than 5 % of documents changed
  since the last fit; FTS5 is always exact. Each committed change writes a new epoch to
  the database and the TF-IDF pickle records the epoch it reflects, so a pickle left behind
  by an interrupted refresh or another agent's write is refit on the next use. With
  `--dense`, documents that have no vector yet are scored on the lexical rankings alone,
  scaled to three rankers, so they are neither buried nor favoured.

The approved plan proposed character n-gram TF-IDF. On about 10,000 documents that
matrix would run to hundreds of megabytes, so stemmed BM25 replaced it for word-variant
robustness. The index is about 100 MB on disk with dense vectors (85 MB SQLite, 20 MB TF-IDF).

## Measured

Measured on 2026-10-19 on a machine running other heavy jobs (load average above 800),
so CPU time is the number to compare; wall time was two to three times larger.

| Check | Result |
|---|---|
| Documents / source files | 10,276 / 2,081 |
| Full build, `cli.py build` (lexical) | 12 s CPU (10 s user, 2 s system); 25 to 32 s wall under that load |
| Dense embeddings for a full build | not re-measured (earlier: about 40 s more) |
| Unchanged refresh | 0.05 s CPU in a running process, 0.15 s in a new one |
| One edited registry record or new handoff section | 0.4 s CPU; TF-IDF patched, not refit |
| CLI query, end to end | about 3 s CPU (2.1 s user, 0.8 s system), lexical |
| Held-out check, top 5 of all kinds | 18/20 lexical, 19/20 with dense |

The held-out cases (`tests/tools/fixtures/corpus_heldout.json`) are 20 negatives added
after 2026-10-04, paraphrased blind by a separate agent that saw only the claims.

## Duplicates

Two checks for negatives that say what an existing record already says
(`duplicates.py`). Both score by TF-IDF cosine (`Corpus.cosine`, the index's own word
unigram and bigram vectors), not by the rank-fusion score a search hit carries, so a score
is a similarity in [0, 1], not a rank. It still depends on the rest of the index through
the IDF weights, and on the fit history: between refits (see Ranking above: more than 5 %
of documents changed) changed documents are patched in with the last fit's vocabulary and
IDF, which can move a score by a few hundredths. On a shared index patched 406 documents past
its fit, the committed report's `COSET-DISTINGUISHABILITY-DEBT-S10/S8-PARTIAL_MATCHING` pair
(0.9002 on a fresh fit) fell just under 0.9, and a `check-new` match within a few thousandths
of 0.6 can flip the same way. `near-duplicates --out` therefore refits first, so the committed report depends only on
the current documents, and its JSON records `changed_since_fit` (0 after that refit);
`build --full` refits the shared index for everything else.

```bash
python tools/corpus/cli.py near-duplicates --out research/audits/registry_duplicates.json --per-family 3
python tools/corpus/cli.py check-new --file draft_record.json      # exit 2: possible duplicate
python tools/corpus/cli.py check-new --text "claim. reason it fails."
```

- `near-duplicates` lists pairs of `negative`-kind documents at or above `--threshold`
  (default 0.9), highest first, at most `--limit` (200). `--per-family N` keeps at most N
  pairs whose two ids differ only in their last `-<number>` (`...-N48-0-1` and
  `...-N48-0-2`). Both take a whole number of at least 0 (argparse exits 2 otherwise):
  `--limit 0` prints the count alone, `--per-family 0` leaves out every such sibling
  pair. The output always gives the count before the limit ("200 of 539 pairs"),
  and the JSON carries it as `total` next to `per_family` and `limit`, with the number of
  `documents` compared, `changed_since_fit`, `index_incomplete` and `index_issues`. `--kind`
  picks another document kind; a kind with no documents is an error (exit 1). When a
  registry file or record cannot be read the command exits 2, like `been-tried`, and with
  `--out` it writes nothing, so a half-written registry never replaces the committed report
  with a shorter one. `--out` must name a `.json` file (exit 1 otherwise, or when it cannot be
  written); it also writes `FILE.md` with the stem upper-cased; the committed report is
  `research/audits/registry_duplicates.json` and `REGISTRY_DUPLICATES.md` (0.9,
  `--per-family 3`: 167 pairs on 2026-10-22, all of them, the same pairs and scores as on
  2026-10-21).
- `check-new` checks one draft claim against the negative records, retained and
  quarantined, at cosine 0.6. It scores every negative-kind document, not only a search's
  top hits, so no record at or above the threshold is missed; the header gives how many
  match, the closest five are listed, and `--json` carries the count as `total`.
  It exits 2 on any match, 0 when there is none, and 1 when
  the draft cannot be used (checked before the index is touched): a `--file` that cannot be
  read, text that starts like a JSON record but is not one (bad or truncated JSON, no string
  `claim`, a `reason_invalid` that is not a string), or a draft with no words to compare
  (empty or only stop words); it also exits 1 when the index holds no negative record at
  all (a `--root` without a registry), rather than calling every claim new. argparse usage
  errors, among them a `--threshold` that is not a number in (0, 1] (for `near-duplicates`
  too), also exit 2, so a hook or script should stop on any status but 0. `--file` takes a text
  file, a registry record as JSON, or a JSON list of records (read as UTF-8, with or without
  a BOM); a record contributes its `claim` and `reason_invalid` (a quarantined record's are
  read from its `original_record`), and is never matched with its own `id` (`negative:ID`
  or `quarantined:ID`; the id is stripped and a `negative:` or `quarantined:` prefix
  dropped). A list is checked record by record, and `--json` marks each match with its
  `draft_id`. A listed record that is not in the index yet is compared with every negative
  record but its own, filed records listed beside it included, so a hunk that copies an
  existing record under a new id exits 2. A listed record already in the index (filed) also
  leaves out the other filed records of the list. Records of one list are therefore not
  compared with each other, the answer is the same before and after the records are filed,
  and a hook can run on the draft or on the new records of the registry edit that files them.
  List only the new records: once a new record is filed, an older record listed beside it is
  hidden from it. When two or more listed records are already filed the command warns on
  stderr, says "no negative record outside the list" for them, and `--json` gives the count as
  `filed`. A draft that reuses another record's id is not compared with that record. A
  quarantined match is labelled `(quarantined)`. An
  unreadable registry is reported on stderr and as `index_incomplete` in `--json` output,
  but does not change the exit code; a hook that must fail closed should check that field.
  `--allow ID` accepts a match the author has read and knows to be a separate result (see
  "How often it fires on distinct records" below).
  The MCP tool `check_duplicate_negative(claim, threshold=0.6, allow=None)` returns the same matches
  for a claim's text, with no id left out, and an `error` for a claim with no words, a
  threshold outside (0, 1] or an index with no negative records.
- The `negative` kind holds retained records (`negative:` ids, 975 today) and quarantined
  ones (`quarantined:` ids, 12). Both are compared and both can match; no quarantined record
  is in a pair at 0.7 or above today.

### Calibration (2026-10-21, this tree: 987 negative-kind documents)

| cosine at least | pairs | pairs grouped by `--per-family` (families) | pairs whose ids are equal up to digits |
|---|---|---|---|
| 0.7 | 1,286 | 90 (10) | 403 |
| 0.8 | 601 | 90 (10) | 324 |
| 0.9 | 207 | 59 (8) | 145 |
| 0.95 | 67 | 15 (4) | 42 |

57 pairs score 1.000. The report default is 0.9: 207 pairs can be read, the 0.8 list is
three times longer, and in the hand check below the pairs under 0.9 are also mostly sweep
siblings. One restatement in the check sits at 0.80, and the default `--limit 200` does not
reach it: with `--threshold 0.8 --per-family 3` the list is "200 of 539 pairs" and that
pair is number 519. When cleaning a specific family, run
`near-duplicates --threshold 0.8 --per-family 3 --limit 1000` and search the output for its
ids.

Hand check of ten pairs across the bands (classes: sweep sibling, one template filled in
for another instance; true restatement, the same claim about the same object filed twice;
distinct, different results that share words):

| cosine | pair | class | why |
|---|---|---|---|
| 1.000 | `NEG-CODE-GOPPA-SCALING-GOPPA-SCALE-M6-T3-N48-0-1` / `...-0-2` | sweep sibling | Same generated text for two code pairs of one Goppa instance; `--per-family` groups them. |
| 1.000 | `NEG-CODE-GOPPA-SCALING-GOPPA-SCALE-M6-T3-N48-0-1` / `...-3-4` | sweep sibling | Same template; the ids differ in two numbers, so `--per-family` does not group them. |
| 1.000 | `LEGACY-BITWISEMAJORITYSECRETFINDING` / `LEGACY-BITWISEXORANDANDSECRETFINDING` | sweep sibling | Two different toy oracles rejected by one template sentence; each name occurs once, so TF-IDF drops it. |
| 0.978 | `QC-AUTOMORPHISM-EQUIVALENT-QC_INDEX4_TWO_CIRCULANTS_TRIAL_11_PRIOR_0` / `QC-AUTOMORPHISM-REJECTED-...` (same trial) | true restatement | The same trial filed under two id prefixes; every field but the id is identical. |
| 0.933 | `QUERY-LOWER-BOUND-GAP-CUBIC_CHIRP` / `...-NOISY_CUBIC_CHIRP` | sweep sibling | One query-lower-bound template run on two hidden-shift families. |
| 0.863 | `COSET-DISTINGUISHABILITY-DEBT-S10-FIXED_POINT_FREE_INVOLUTION` / `...-S16-...` | sweep sibling | One copy-debt template at n = 10 and n = 16; only the evidence numbers differ. |
| 0.816 | `NEG-QUARANTINE-MUT-CAND-DHS-GOWERS-SIEVE-QUERY-MODEL-HARDENED` / `NEG-QUARANTINE-MUT-CAND-HYP-LIT-HIDDEN-SHIFT-SIEVE-QUERY-MODEL-HARDENED` | sweep sibling | One interface-audit template for two different mutation candidates. |
| 0.803 | `CLOSURE-REJECT-CLOSURE_BCH_CODE_SEARCH_BCH_M5_D3_11_S3_D4__BCH_M5_D3_11_S11_D5` / `SCHUR-REJECT-SCHUR_BCH_...` (same pair) | true restatement | The same BCH pair is declared not a hard row twice, by the closure and by the Schur invariant; one record with two reasons would do. |
| 0.773 | `NEG-ORTHOGONAL-PARABOLIC-DEQUANTIZATION-BOUND` / `NEG-UNITARY-PARABOLIC-DEQUANTIZATION-BOUND` | distinct | Parallel hand-written results for orthogonal and unitary groups, each with its own classical algorithm and density bound. |
| 0.724 | `CODE-FRONTIER-TRIAGE-CYCLIC_FAMILY_CYCLIC_N15` / `CODE-FRONTIER-TRIAGE-GOPPA_FAMILY_GOPPA_M4_T2` | sweep sibling | One triage template over two code families. |

Seven sweep siblings, two true restatements, one distinct pair.

**Sweep-sibling caveat.** Most of the registry's close pairs are generated records, one
per instance, whose only difference is the instance name. A name that occurs in a single
record is not in the TF-IDF vocabulary (`min_df` 2), so such pairs score up to 1.000.
`--per-family` groups only ids that differ in their last `-<number>`: 59 of the 207 pairs
at 0.9, while 145 of them have ids that are equal once digits are ignored and others differ
by a word (`CUBIC_CHIRP` and `NOISY_CUBIC_CHIRP`). A family key that ignores every digit
was measured and not adopted: at 0.8 with a cap of 3 it shortens the list from 539 to 403
pairs, but the 0.80 restatement only moves from number 519 to 385, still past the first 200.
Read a pair before merging records; a sweep sibling is a separate result and should stay.

**`check-new` threshold.** Each of the 975 retained negatives was checked against itself.
Its claim plus reason scores at least 0.6 with its own record every time (minimum 0.660,
median 0.840); its claim alone does so for 92 % (97 % when the reason is at most 300
characters, 51 % above 300, 16 % above 600, the long hand-written records). End to end
through `check_claim` on 163 sampled records: own record found from claim plus reason
163/163, from the claim alone 152/163. Three unrelated claims scored 0.06, 0.12 and 0.16
against their nearest negative. So 0.6 stays, and the input should be the claim and its reason, as `--file` does with a
record.

**How often it fires on distinct records.** The checks above measure recall. Specificity,
measured on 2026-10-22 by refiling each of the 975 retained negatives as filed (its own id
left out), is low for generated records:

| threshold | records that exit 2 | top match's id equal up to digits | first three id tokens shared | first two shared | other |
|---|---|---|---|---|---|
| 0.6 | 401 (41 %) | 209 | 120 | 27 | 45 |
| 0.65 | 353 (36 %) | 200 | 82 | 26 | 45 |
| 0.7 | 284 (29 %) | 164 | 57 | 24 | 39 |
| 0.8 | 102 (10 %) | 64 | 5 | 14 | 19 |

At 0.6, 340 of the 401 have the same `reason_invalid`, word for word, as their closest
match, and 39 of the 45 "other" are `LEGACY-*SECRET*` toy-oracle template records: sweep
siblings, which the caveat above says should stay. Hand-written records fare better: of the
409 `NEG-` records outside the generated `NEG-CODE-` and `NEG-QUARANTINE-MUT-` families, 17
exit 2, 15 of them siblings inside the `NEG-SELF-DUAL-WREATH` program (0.60 to 0.72) and two
the orthogonal and unitary parabolic pair classed distinct above. Raising the threshold does
not fix this (0.7 still blocks 284) and costs claim-alone recall. Instead, after reading a
sibling, pass `--allow ID`, or `--allow PREFIX*` for its family (repeatable; the MCP tool takes
`allow`): its matches are then listed as allowed, each with its cosine, and do not count toward
the exit code. When every match is allowed the header says that no record outside `--allow`
reaches the threshold and how many allowed ones do. A bare `*` is rejected.

Smoke runs on this checkout (2026-10-21):

| input | exit | top match (cosine) |
|---|---|---|
| `--text` claim of `COSET-DISTINGUISHABILITY-DEBT-S10-FIXED_POINT_FREE_INVOLUTION` | 2 | that record (0.701) |
| `--file` that record under a new id | 2 | that record (0.850), then its S8 sibling (0.785) |
| `--file` that record as filed | 2 | its S8 sibling (0.785); its own id is left out |
| `--text` claim of `NEG-QAOA-BOUNDED-DEPTH-OPTIMIZATION-BARRIER` | 0 | none: a long reason, claim alone below 0.6 |
| `--text` claim and reason of that record | 2 | that record (0.775) |
| `--file` that record as filed | 0 | none: no other record is that close |
| `--file` `NEG-UNITARY-PARABOLIC-DEQUANTIZATION-BOUND` as filed | 2 | the orthogonal one (0.664) |
| `--text "Grover search gives a quadratic speedup for unstructured search."` | 0 | none |
| `--text` claim and reason of quarantined `NEG-QUANTUM-ANNEALING-SPECTRAL-GAP-BARRIER` | 2 | that record, labelled `(quarantined)` (0.924) |
| `--file /nonexistent/draft.json` | 1 | none: `error: cannot read ...` on stderr |
| `--file` quarantined `NEG-QUANTUM-ANNEALING-SPECTRAL-GAP-BARRIER` as filed (2026-10-22) | 0 | none: its claim is read from `original_record` and its own id left out |
| `--file` `NEG-UNITARY-PARABOLIC-DEQUANTIZATION-BOUND` as filed `--allow NEG-ORTHOGONAL-PARABOLIC-DEQUANTIZATION-BOUND` (2026-10-22) | 0 | none counted; the orthogonal one listed as allowed |

## Baselines

Which classical algorithm should a quantum idea be compared against first? `baselines.py`
ranks a curated catalog, `tools/corpus/baselines.json` (15 entries), against a short
description of the idea.

```bash
python tools/corpus/cli.py baselines "sampling the Gibbs law of a signed parity-check code"
python tools/corpus/cli.py baselines "DQI for max-k-cut on a ternary cycle code" -k 3 --json
```

Each result shows the baseline's name and id, its score, why it was chosen (the keywords
matched and the notes or negatives that name it, with `file:line`), its summary, its
references and, when the repository can run it, a `run:` command that runs it as printed,
or a `call:` line naming the library function that computes it on an instance
(`prange-restarts-opi`: `tools/dqi_screen/prange.py:prange_restarts`). `--json` prints
`{"idea", "recommendations": [{"baseline", "score", "matched", "evidence"}], "index_incomplete", "index_issues"}`
with each evidence hit in the `search --json` shape. The MCP tool
`classical_baselines(idea, k=5)` returns the same object.

**Score.** `tokens(t)` lower-cases `t`, writes umlauts as ae/oe/ue and drops other accents,
keeps the runs of `[a-z0-9]` and makes each word singular:
a final `sses` becomes `ss`, a final `ies` becomes `y` in words longer than four letters
("parities" is `parity`), "bases" is `basis` and a word ending in `sis` keeps its `s`, and
otherwise a final single `s` is dropped from words longer than three letters ("Gibbs" becomes
`gibb` on both sides; "glasses" and "glass" both become `glass`). It then folds a few
spelling variants and abbreviations into one (`_SPELLINGS`: "colouring" is `coloring`,
"Gröbner" and "Grobner" are `groebner`, "MaxCut" is `max cut`, and the notes' OPI, MQ, LPN,
CVP and USD are the phrases the keywords spell out, so "mixed-coset OPI" matches `optimal
polynomial intersection`). A mechanism
keyword matches when every one of its tokens is among the idea's tokens, in any order. A `k`
in a keyword stands for a number: such a keyword must occur in a row with a number, `k` or
`q` in that place, so `max k cut` matches "max-3-cut" and "Max-q-Cut" but not "max cut at
depth 3". The ten
note sections and negatives that `search` ranks nearest the idea are read in full; one cites a
baseline when the baseline's name or an alias occurs in its title or text, case-insensitively
and on word boundaries. A mention inside a longer name of another baseline counts only for
that one: "Prange" inside "USD-Prange" or "product-USD/Prange" cites the USD-Prange sampler,
not `prange-isd` (on "p-spin Gibbs sampling" such mentions had put `prange-isd` first, at 0.5,
on citations alone). Notes are indexed by section, so a note counts once however many of
its sections are among the ten, and its nearest citing section is the evidence shown. Each
negative counts on its own, although all of them live in one registry file.

    score = matched keywords / keywords + citing notes and negatives / 10        (rounded to 4 places)

Baselines scoring 0 are left out; the rest are sorted by score, then name, and the first `k`
(default 5) are shown. The CLI rejects a `-k` below 1 (with 0 it would show nothing and then
say that no baseline matches), and the Python and MCP calls return nothing for one. A score
can exceed 1. A citing note may name a baseline only to set it
aside, and keywords are matched without regard to how the idea uses them, so the score orders
leads to read and run. It is not evidence that the baseline beats the idea, and an empty list
does not mean that no classical baseline applies.

Smoke run on this checkout (2026-10-21), `baselines "sampling the Gibbs law of a signed
parity-check code"`:

| rank | baseline | score | why |
|---|---|---|---|
| 1 | `polar-sc-source-shaping` | 0.5 | gibbs sampling, signed parity; named by `RESEARCH_PRIORITY_DECISION.md` |
| 2 | `usd-prange-rejection-sampler` | 0.5 | gibbs sampling, parity check; named by one registry negative |
| 3 | `prange-isd` | 0.4 | parity check; named by that negative and `COHERENT_BPQM_ERASURE.md` |
| 4 | `stochastic-localization-pspin` | 0.2 | gibbs sampling |

`baselines "DQI for max-k-cut on a ternary cycle code" -k 3` ranks `lp-decoding-cycle-codes`
first (0.4: cycle code, max k cut), then `sdp-relaxation` (0.3: max cut, named by
`QAOA_BOUNDED_DEPTH_OPTIMIZATION_BARRIER.md`) and `tensor-network-simulation` (0.1). When
every section counted, four sections of that one note gave `sdp-relaxation` 0.6 and put it
above the LP decoder, the baseline this line of work is missing. The same order holds for
"max-3-cut" (2026-10-22); before the `k` placeholder, that spelling missed `max k cut` and
put `sdp-relaxation` (0.3) above the LP decoder (0.2).

**Schema.** `{"baselines": [entry, ...]}`, each entry with every field below:

| field | content |
|---|---|
| `id` | unique kebab-case id |
| `name`, `aliases` | the names a note would use; matched case-insensitively on word boundaries, and a hyphen is a boundary, so avoid short common words and phrases that occur in other terms ("norm construction" matched "low-norm Construction-A", so the alias is "classical norm construction") |
| `problem` | the problem the algorithm solves, one sentence |
| `mechanisms` | 3 to 6 lowercase keywords an idea would contain |
| `summary` | what the algorithm does and what it is the baseline for |
| `references` | a list of `{"arxiv": "2609.40036"}` or `{"note": "STEM"}` (the file `research/STEM.md`, which must name the baseline or an alias) |
| `runnable` | `null`, or `{"command": ..., "entry": ...}` with at least one: a command that runs the baseline from the repository root as printed, and a `path.py:function` |

**Adding an entry.** Append it to `baselines.json`, raise the count in
`test_catalog_is_well_formed`, then run `python -m pytest -q tests/tools/test_corpus_baselines.py`.
`validate_catalog` reports an entry that is not an object, a duplicate id, a missing or
mistyped field, a blank name or alias, fewer than 3 or more than 6 keywords, a keyword that
is not lowercase or that `tokens` cannot match as written (`"-"` has no word and would match
every idea; the `χ` of `"χ² test"` would be dropped, so spell keywords in ASCII, although
accents fold and `"gröbner basis"` is fine), a `runnable` other than `null` or
`{command?, entry?}`, and a malformed reference. `recommend`, the CLI and the MCP tool refuse
a catalog with any such problem, or one that cannot be read or parsed as
`{"baselines": [...]}`: the CLI prints `error: ...` on stderr and exits 1, and the MCP tool
returns `{"error"}`. The tests also check that every note reference
exists as `research/<STEM>.md` and names its baseline (its name or an alias), that every
runnable entry is a function defined in that file, and that every runnable command exits 0
when run from the repository root (it skips only in a checkout without `tools/dqi_screen/`).

Three entries cite no note: no committed note discusses stochastic localization, Prange
completion as a finite-length OPI baseline, or LP decoding of cycle codes
(`TERNARY_PREFIX_INTEGRALITY` uses a certified LP to prune ternary prefixes, a different
LP). They cite their papers instead.

**Notes to add back when present.** Three notes that belong in the catalog are uncommitted
agent edits in the main checkout, so no entry references them yet. Add each to its entry once
it is committed:

| note | likely entry | why |
|---|---|---|
| `TERNARY_COLORING_BPQM` | `lp-decoding-cycle-codes` | The q = 3 cycle-code line whose missing baseline is the LP decoder of arXiv:2609.40036 (`research/audits/ARXIV_TRIAGE_REVIEWED.md`). |
| `BALANCED_SIGNED_MPI` | `prange-restarts-opi` | Multiplicative polynomial intersection with a signed objective, screened against the Prange line. |
| `CUBIC_ORBIT_DECODER` | not chosen | Read the note first. |

`FOLDED_NORM_MQ` was the fourth such note; it is committed now and `groebner-mq` cites it.
