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
2,100 source files and re-parses only those whose size, mtime and content hash changed
(about 0.1 s when nothing changed). Add `--json` for machine-readable output,
`--dense` to add the embedding ranker, `--root PATH` (or `QSEARCH_ROOT`) to index
another checkout.

## For the research agents (MCP)

`tools/corpus/mcp_server.py` is a stdio MCP server exposing `been_tried`,
`search_corpus` and `get_doc`. It keeps the index warm, refreshes it at most every 30
seconds, and uses dense embeddings automatically once `build --dense` has run. Point
each agent's own configuration at it; nothing in the repository needs to change.

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
  survive new sections being added on top. Theorem modules are summarized from their
  docstrings with `ast`, never imported. A file that fails to parse (one committed
  hypothesis contract currently has an invalid JSON escape) is indexed as raw text with
  status `unparseable`.
- **Storage** (`store.py`): `research/corpus_index/corpus.sqlite` (WAL) holds file
  states, documents, an FTS5 table and dense vectors keyed by content hash. The directory
  ignores itself in git.
- **Ranking** (`ranking.py`): SQLite FTS5 BM25 with the Porter stemmer, plus word
  unigram/bigram TF-IDF cosine, fused by reciprocal rank. Optional third ranker: local
  `sentence-transformers/all-MiniLM-L6-v2` embeddings (offline once cached). TF-IDF is
  patched incrementally and refit when more than 5 % of documents changed since the last
  fit; FTS5 is always exact.

The approved plan proposed character n-gram TF-IDF. On about 10,000 documents that
matrix would run to hundreds of megabytes, so stemmed BM25 replaced it for word-variant
robustness. The index is about 70 MB on disk.

## Measured

| Check | Result |
|---|---|
| Documents / source files | 10,275 / 2,081 |
| Full build | 8 s lexical, about 40 s more for dense embeddings |
| Unchanged refresh | 0.1 s |
| CLI query, end to end | 1.4 s lexical, 4.3 s dense (model load) |
| Held-out check, top 5 of all kinds | 18/20 lexical, 19/20 with dense |

The held-out cases (`tests/tools/fixtures/corpus_heldout.json`) are 20 negatives added
after 2026-10-04, paraphrased blind by a separate agent that saw only the claims.
