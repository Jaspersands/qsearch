# Spend accounting

What does the research loop cost? These tools answer it as far as the data allows. They read
the registry and git history and never write to `research/registry/`. Their outputs go to
`research/audits/`.

```bash
python tools/spend/timed.py -- python qsearch.py <subcommand> ...   # time one run (opt-in)
python tools/spend/ledger.py      # rebuild the code-free part of the ledger
python tools/spend/tokens.py      # add per-day Codex token totals (--dry-run to preview)
python tools/spend/report.py      # write SPEND_REPORT.md and spend_summary.json
```

Run them in that order: `report.py` reads only the ledger.

## The timing wrapper

Put `python tools/spend/timed.py --` in front of any command:

```bash
python tools/spend/timed.py -- python qsearch.py validate
python tools/spend/timed.py --label gemini-1 -- python qsearch.py <subcommand> ...
```

- The command runs as usual. Its output is not captured, and the wrapper exits with the
  command's exit code (128+N if signal N killed it, 127 if the command was not found).
- Afterwards it appends one `timed_run` line to `research/audits/spend_ledger.jsonl`. The
  line holds wall time, CPU time, peak memory, the exit code and the registry counts before
  and after the run.
- `--label` is free text, for example which agent ran the command. `--ledger` writes
  somewhere else, which tests use.

## Ledger schema

`research/audits/spend_ledger.jsonl` holds one JSON object per line, sorted by time. Every
line has `kind`, `timestamp` (UTC, ISO 8601, to the second) and `source`.

| kind | Written by | Other fields |
|---|---|---|
| `experiment_run` | `ledger.py` | `run_id`, `experiment_id`, `candidate_id`, `status`, `falsifier_count`, `negatives_written` (the run's `negative_results_written` metric, or null) |
| `theorem_commit` | `ledger.py` | `sha` (12 chars), `path` (a `theorems/*.py` file), `change` (A added, M modified, D deleted) |
| `registry_commit` | `ledger.py` | `sha`, `negatives` (count at that commit), `negatives_delta` (change from the previous commit), `negatives_new` (ids first seen here), `negatives_new_retained` (of those, ids still in the registry today) |
| `registry_uncommitted` | `ledger.py` | `negatives`, `negatives_new_retained` (ids in the working-tree registry that no commit has yet); the timestamp is the file's mtime |
| `report_write` | `ledger.py` | `path` (a report json under `research/`), `theorem` (the theorem file whose `REPORT*` constant names it); the timestamp is the file's mtime |
| `timed_run` | `timed.py` | `ended_at`, `command` (repo paths made relative), `subcommand`, `label`, `wall_seconds`, `cpu_seconds` (`cpu_user_seconds` + `cpu_system_seconds`), `peak_rss_bytes`, `exit_code`, `registry_before`, `registry_after` (records per `research/registry/*.json`, null if unreadable), `registry_delta` (non-zero changes only), `negatives_added` |
| `token_day` | `tokens.py` | `date`, `agent` (`codex`), `sessions`, `input_tokens`, `cached_input_tokens`, `output_tokens`, `reasoning_output_tokens`, `total_tokens` |

`ledger.py` replaces only its own five kinds and `tokens.py` only `token_day`, so timed runs
survive every rebuild. Writers lock the file, so an agent can append a timed run during a
rebuild.

`spend_summary.json` is a per-day digest for the cockpit, in this fixed shape:
`{"generated_on", "days": [{"date", "runs", "wall_seconds", "cpu_seconds", "negatives_added", "tokens"}]}`.
Days are UTC.

## What each source can and cannot tell you

- **Run history timestamps** say when a run was recorded and what it decided. There is one
  timestamp per run and no start time, so they give runs per day but not how long a run took.
  The `negative_results_written` metric is set by only some runs: it sums to 652 against 976
  retained negatives.
- **Commit times** say when work was saved to git, not when it was done or how long it took.
  Commits are batched, sometimes days after the work. The first commit of a file back-fills
  everything before it: the first registry commit holds 459 negatives, and the first theorem
  commit adds 724 theorem files. Dating negatives by their first commit is the most complete
  count of negatives per day, but it shows when they were committed, which can be days after
  they were made.
- **Report-file mtimes** are the last time the file was written, not the first. A fresh
  checkout or worktree resets them all to checkout time. In this worktree all 398 fall in the
  same hour, so the report keeps them out of its tables. They mean something only in a
  long-lived checkout where agents write the files.
- **Timed runs** are the only measured durations. Wall time is the clock time of the command.
  CPU time is user plus system time of the command and the children it waited for, and can
  exceed wall time with threads. Peak RSS is the largest resident set among those processes.
  The registry delta counts every writer during the run, including other agents working at
  the same time. Days without a timed run show `wall_seconds` 0.0 and `cpu_seconds` null:
  unmeasured, not free.
- **Runs per day** in the report counts run-history runs plus timed runs. A timed run that
  logged an experiment run inside its own time window is counted once.

## Token logs

Checked on 2026-10-19, reading only key names and numbers:

- **Codex records token counts.** Session logs (`~/.codex/sessions/`, and
  `~/.codex/archived_sessions/` as `.jsonl.zst`) contain a `token_count` event after each
  model call. Each event carries the session's cumulative input, cached-input, output and
  reasoning tokens. `tokens.py` keeps sessions whose starting directory is this repo (9 of
  71 files). It sums each session's increases in the cumulative total per UTC day. The first
  event of a session, and any event where the total drops, count their own usage instead, so
  forked sessions do not re-count their parent. It writes per-day totals only: no text, paths
  or ids. Reading `.zst` archives needs the `zstandard` module; without it they are skipped
  and counted.
- **Gemini does not record usable token counts.** The Gemini CLI keeps chats under
  `~/.gemini/tmp/`, which does not exist here. The Antigravity app in `~/.gemini/antigravity`
  has no token-named field in its JSON, JSONL or logs, and no such column in its SQLite
  files. Its per-generation metadata (`conversations/*.db`, table `gen_metadata`) is
  unlabelled protobuf. Some integer fields there might be token counts, but without a schema
  that is a guess, so nothing is imported.

So `tokens` in the summary is Codex only, and null on days without a Codex record. Over
2026-07-06 to 2026-10-18 the Codex total is 5.47 billion tokens. 97% of that is cached input
re-sent each turn; uncached input plus output is about 173 million. Tokens per negative leave
out the Gemini agents, so they are a lower bound for the loop.
