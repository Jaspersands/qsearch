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
| `near-duplicates [--threshold 0.9] [--per-family N] [--out FILE.json]` | Pairs of negatives with a high TF-IDF cosine (see Duplicates). |
| `check-new --text CLAIM \| --file RECORD.json [--threshold 0.6]` | Exit 2 when a draft negative is close to a retained one. |

Every command except `build` first refreshes the index incrementally: it stats about
2,100 source files and re-parses only those whose size, mtime and content hash changed.
When nothing changed the refresh only reads (no write lock) and costs 0.05 to 0.15 s of
CPU. Add `--json` for machine-readable output, `--dense` to add the embedding ranker,
`--root PATH` (or `QSEARCH_ROOT`) to index another checkout.

A file or registry record that cannot be parsed is never silent. Every command prints the
problem on stderr and JSON output carries `index_issues`. When the problem is in
`research/registry/` (say a half-written `negative_results.json`), `index_incomplete` is
true, `been-tried` prints INDEX INCOMPLETE and exits with status 2: an empty "Killed
before" group then means the registry could not be read, not that the idea is new.

## For the research agents (MCP)

`tools/corpus/mcp_server.py` is a stdio MCP server exposing `been_tried`,
`search_corpus`, `get_doc` and `check_duplicate_negative` (the `check-new` check, below).
It keeps the index warm and refreshes it at most every 30
seconds. With the default `--dense auto` it adds the embedding ranker only while every
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
is a similarity in [0, 1] whatever else is in the index.

```bash
python tools/corpus/cli.py near-duplicates --out research/audits/registry_duplicates.json --per-family 3
python tools/corpus/cli.py check-new --file draft_record.json      # exit 2: possible duplicate
python tools/corpus/cli.py check-new --text "claim. reason it fails."
```

- `near-duplicates` lists pairs of `negative`-kind documents at or above `--threshold`
  (default 0.9), highest first, at most `--limit` (200). `--per-family N` keeps at most N
  pairs whose two ids differ only in their last `-<number>` (`...-N48-0-1` and
  `...-N48-0-2`). `--out FILE.json` also writes `FILE.md` with the stem upper-cased; the
  committed report is `research/audits/registry_duplicates.json` and
  `REGISTRY_DUPLICATES.md` (0.9, `--per-family 3`: 167 pairs on 2026-10-21).
- `check-new` checks one draft claim against retained negatives at cosine 0.6 and exits 2
  on any match, 0 otherwise, so it can gate a hook or a script. `--file` takes a text file
  or a registry record as JSON; a record contributes its `claim` and `reason_invalid`. An
  unreadable registry is reported on stderr and as `index_incomplete` in `--json` output,
  but does not change the exit code; a hook that must fail closed should check that field.
  The MCP tool `check_duplicate_negative(claim, threshold=0.6)` returns the same matches.
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
siblings. One restatement in the check sits at 0.80, so run `--threshold 0.8` when
cleaning a specific family.

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
by a word (`CUBIC_CHIRP` and `NOISY_CUBIC_CHIRP`). Read a pair before merging records; a
sweep sibling is a separate result and should stay.

**`check-new` threshold.** Each of the 975 retained negatives was checked against itself.
Its claim plus reason scores at least 0.6 with its own record every time (minimum 0.660,
median 0.840); its claim alone does so for 92 % (97 % when the reason is at most 300
characters, 51 % above 300, 16 % above 600, the long hand-written records). End to end
through `check_claim` on 163 sampled records: own record found from claim plus reason
163/163, from the claim alone 152/163. Three unrelated claims scored 0.06, 0.12 and 0.16
against their nearest negative. So 0.6 stays, and the input should be the claim and its reason, as `--file` does with a
record.

Smoke runs on this checkout (2026-10-21):

| input | exit | top match (cosine) |
|---|---|---|
| `--text` claim of `COSET-DISTINGUISHABILITY-DEBT-S10-FIXED_POINT_FREE_INVOLUTION` | 2 | that record (0.701) |
| `--file` that record | 2 | that record (0.850), then its S8 sibling (0.785) |
| `--text` claim of `NEG-QAOA-BOUNDED-DEPTH-OPTIMIZATION-BARRIER` | 0 | none: a long reason, claim alone below 0.6 |
| `--file` that record | 2 | that record (0.775) |
| `--file` `NEG-UNITARY-PARABOLIC-DEQUANTIZATION-BOUND` | 2 | that record (0.855), then the orthogonal one (0.664) |
| `--text "Grover search gives a quadratic speedup for unstructured search."` | 0 | none |
