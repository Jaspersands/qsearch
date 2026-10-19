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
`search_corpus` and `get_doc`. It keeps the index warm and refreshes it at most every 30
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
