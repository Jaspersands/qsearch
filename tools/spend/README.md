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

`ledger.py` and `tokens.py` rewrite their own kinds of line, so they refuse (exit 3, nothing
written) when the data they would rebuild from is missing here, rather than overwrite
history with less:

- `ledger.py` refuses in a checkout without git history or with a shallow one (CI's default
  `actions/checkout` is shallow).
- Both refuse when the rebuild would drop more than 20% of the existing lines of one of their
  kinds (only kinds with at least 5 lines are checked). That means a missing run history,
  pruned Codex logs or similar.
- `tokens.py` refuses when it had to skip `.jsonl.zst` logs because the `zstandard` module is
  missing. Most Codex logs are `.zst`, so install it first: `pip install zstandard`. It is not
  in `requirements-tools.txt`, so CI skips the test that reads `.zst` files
  (`test_import_reads_zstd_archives`).

`--force` writes anyway; `tokens.py --dry-run` never writes and only warns.

## The timing wrapper

Put `python tools/spend/timed.py --` in front of any command:

```bash
python tools/spend/timed.py -- python qsearch.py validate
python tools/spend/timed.py --label gemini-1 -- python qsearch.py <subcommand> ...
```

- The command runs as usual. Its output is not captured, and the wrapper exits with the
  command's exit code (128+N if signal N killed it, 127 if the command was not found, 126 if
  it could not be executed). It writes a ledger line in every case.
- Afterwards it appends one `timed_run` line to `research/audits/spend_ledger.jsonl`. The
  line holds wall time, CPU time, peak memory, the exit code and the registry counts before
  and after the run.
- The ledger is committed, so the command is recorded sanitized: the program by name
  (`python3`, not its path), repo files relative to the repo (files in the main checkout too,
  when run from a worktree), any other absolute or `~` path as `<path>` (inside a longer
  argument too, such as code after `-c`), and the values of `NAME=VALUE` arguments and of
  options whose name contains token, key, secret, passw, auth or credential as `<redacted>`.
  `subcommand` is the qsearch subcommand for `qsearch.py <subcommand>` and null otherwise.
  `ledger.py` re-applies the same sanitizer to the timed lines it keeps, so a line written by
  an older wrapper is cleaned on the next rebuild.
- SIGTERM and SIGHUP sent to the wrapper are passed on to the command. So is SIGINT, unless
  the wrapper and the command are in the terminal's foreground process group: a Ctrl-C has
  then reached the command already, and a second one could cut its cleanup short. (So a
  `kill -INT` aimed at a wrapper running in the foreground of a terminal is not passed on.)
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
| `report_write` | `ledger.py` | `path` (a report json under `research/`), `theorem` (the theorem file whose `REPORT*` constant names it); the timestamp is the file's mtime in the checkout that ran `ledger.py` |
| `timed_run` | `timed.py` | `ended_at`, `command` (sanitized, see above), `subcommand`, `label`, `wall_seconds`, `cpu_seconds` (`cpu_user_seconds` + `cpu_system_seconds`), `peak_rss_bytes` (null if the command could not start), `exit_code`, `registry_before`, `registry_after` (records per `research/registry/*.json`, null if unreadable), `registry_delta` (non-zero changes only), `negatives_added` (the raw change in the negatives registry's record count during the run) |
| `token_day` | `tokens.py` | `date`, `agent` (`codex`), `sessions`, `input_tokens`, `cached_input_tokens`, `output_tokens`, `reasoning_output_tokens`, `total_tokens` |

`ledger.py` replaces only its own five kinds and `tokens.py` only `token_day`, so timed runs
survive every rebuild. Writers lock the file, so an agent can append a timed run during a
rebuild.

`spend_summary.json` is a per-day digest for the cockpit, in this fixed shape:
`{"generated_on", "days": [{"date", "runs", "wall_seconds", "cpu_seconds", "negatives_added", "tokens"}]}`.
Days and `generated_on` are UTC dates. `runs` counts experiment runs only; timed commands
are counted apart in the report.

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
  checkout or worktree resets them all to checkout time. The committed `report_write` lines
  come from the checkout that last ran `ledger.py` (the `corpus-substrate` worktree), so they
  change with every checkout that rebuilds the ledger. There all 398 fall in the same hour, so
  the report keeps them out of its tables. They mean something only in a long-lived checkout
  where agents write the files.
- **Timed runs** are the only measured durations. Wall time is the clock time of the command.
  CPU time and peak RSS come from `wait4` on the command itself: user plus system time of the
  command and the children it waited for (it can exceed wall time with threads), and the
  largest resident set among those processes. They do not include earlier children of
  whatever called `run_timed`. On Linux, that process-lifetime high-water mark may include
  memory inherited from the launcher before exec; it does not isolate allocations after
  exec. The registry delta counts every writer during the run,
  including other agents working at the same time, so it is a raw count change, not a count
  of retained negatives. Days without a timed run show `wall_seconds` 0.0 and `cpu_seconds`
  null: unmeasured, not free.
- **Runs per day** in the report are experiment runs from the run history. Timed commands are
  counted separately, because any command can be timed (`qsearch.py validate` is not an
  experiment run); an experiment run made through the wrapper appears in both counts.

## Token logs

Checked on 2026-10-19, reading only key names and numbers:

- **Codex records token counts.** Session logs live in `~/.codex/sessions/` and
  `~/.codex/archived_sessions/`. Both hold `.jsonl.zst` files: here 60 of the 64 files in
  `sessions/` and all 7 in `archived_sessions/` are compressed, and reading them needs the
  `zstandard` module (without it they are skipped and counted, and `tokens.py` refuses to
  write). The logs contain a `token_count` event after each model call. Each event carries
  the session's cumulative input, cached-input, output and reasoning tokens. `tokens.py`
  keeps sessions whose starting directory is this repo (9 of 71 files). It sums each
  session's increases in the cumulative total per UTC day. The first counted event of a
  session, and any event where the total drops, count their own usage instead.
- **Forks replay their parent.** A forked session (`session_meta.forked_from_id`) starts its
  log with a copy of the parent's `token_count` history from zero, re-stamped at fork time.
  Counted as is, the parent's usage would be counted twice, the second time on the fork's day:
  here 3 of the 4 forks do this, 416 events and 52,157,931 tokens. `tokens.py` skips that
  replayed prefix: the leading events whose cumulative totals also occur in the parent's log
  (or, when the parent's log is gone, in an in-project session that started earlier), and
  counts the fork from the end of the prefix. The parents kept running after they were forked,
  so the prefix ends well before the parent's final total; comparing with the final total
  would drop the forks' own usage. The fourth fork's log carries the same session id as another
  fork and starts from that session's final total, so it replays nothing and is counted as is.
- **Bad records are skipped, not fatal.** A torn last line (a session still being written), a
  `token_count` without a timestamp or with a non-numeric count is skipped and counted in
  `bad_lines`; a `.zst` file that ends early keeps what was read and is counted in `truncated`.
- `tokens.py` writes per-day totals only: no text, paths or ids. Session ids are read only to
  match a fork to its parent, in memory.
- **Gemini does not record usable token counts.** The Gemini CLI keeps chats under
  `~/.gemini/tmp/`, which does not exist here. The Antigravity app in `~/.gemini/antigravity`
  has no token-named field in its JSON, JSONL or logs, and no such column in its SQLite
  files. Its per-generation metadata (`conversations/*.db`, table `gen_metadata`) is
  unlabelled protobuf. Some integer fields there might be token counts, but without a schema
  that is a guess, so nothing is imported.

So `tokens` in the summary is Codex only, and null on days without a Codex record. Over
2026-07-06 to 2026-10-18 the Codex total is 5.44 billion tokens. 97% of that is cached input
re-sent each turn; uncached input plus output is about 169 million. The report's tokens per
retained negative divides all of them by every retained negative dated in that window (976),
days without a token record included. It is a Codex-only figure: the Gemini agents' tokens
are missing and nothing here says how many there were, so it is not a bound on the whole
loop.
