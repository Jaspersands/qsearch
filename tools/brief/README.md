# Agent brief

One page for the start of an agent session: what changed in the last week, what is waiting
on the agents, and the five checks to run before choosing or committing a direction.

```bash
python tools/brief/build_brief.py
```

That writes `research/audits/AGENT_BRIEF.md` and `research/audits/agent_brief.json`. Line for
each agent's standing prompt:

*Read research/audits/AGENT_BRIEF.md before choosing a direction.*

```bash
python tools/brief/build_brief.py --since-days 14            # a longer window
python tools/brief/build_brief.py --out DIR                  # write both files into DIR instead
python tools/brief/build_brief.py --json                     # also print the brief as JSON
python tools/brief/build_brief.py --root ../other-checkout
```

It exits 0 whatever it finds; a `--root` that is not a directory, a `--since-days` outside 1
to 3650, or an output directory that is not a writable directory (checked before the build) is
a usage error (exit 2), and `build()` raises `ValueError` for such a window. A write that fails
anyway (a full disk) also exits 2, with one line. Each file is written beside itself and renamed
into place, `agent_brief.json` first, so an agent reading the brief while it is rebuilt sees
the old file or the new one, never an empty or cut-short one. The
window runs from 00:00 local time on the day `--since-days` before today's local date
(default 7); a `today` passed to `build()` as a datetime counts as its local date.

**Local time.** The sources stamp local calendar dates (`dt.date.today()`): the arXiv watch's
`first_seen`, the verdicts' and the referee's `reviewed_on`, the referee queue's "Generated
on". The brief compares those stamps with its window, so it dates by the same clock: the page
never shows a review dated after its own date, and a verdict stamped on the cutoff day is in
the window. The header names the zone (`00:00 local time, UTC+11:00`), `agent_brief.json` has
it as `window_start`, and git gets the cutoff converted to UTC, with the offset of the cutoff
day itself. Run the brief in the zone the stamps were made in; the scheduled watch in CI
(06:00 UTC on Mondays) stamps the same calendar date as local time anywhere from UTC-06:00 to
UTC+17:00.

## Why it exists

The agents are good at proposing and weak at checking, and the checks that exist sit in files
nothing reads at the start of a session: 22 flagged arXiv papers got human verdicts whose
actions are addressed to the agents (`research/audits/arxiv_verdicts.json`), the referee's
flags live in `REFEREE_QUEUE.md`, the cockpit's inertia flags in `site/data/cockpit.json`, and
preflight only helps when someone runs it. The brief puts each of them on one page.

## Sections

| Section | Reads | Shows |
|---|---|---|
| Registry | `research/registry/negative_results.json` in the working copy and at its last change before the window (git) | ids added and removed; removed ids now in `quarantined_campaign_negatives.json` are named as quarantined (when that file cannot be read, or a directory or dangling link sits at its path, the page says so rather than "0 now in the quarantine file") |
| arXiv watch | `research/audits/arxiv_collisions.json`, `research/audits/arxiv_verdicts.json` (via `tools/arxiv_watch/verdicts.py`) | possible kills and scoops with no verdict (however old), flagged papers first seen in the window with their verdict, every verdict recorded in the window by id (in the flagged table, or in a list after the tally for papers the table does not show, such as a kill on a paper first seen before the window), and every verdict action not marked `"action_done": true` (only a JSON `true` closes one). Without a readable `arxiv_collisions.json` the flag counts and table say not available, and the verdicts and actions still show |
| Referee | `tools/referee/referee.py` `status()` over `research/audits/reviews/reviews.json` | notes flagged unsound or needs-work with their worst claim, and stale reviews |
| Preflight | `tools/preflight/preflight.py` `run()`, the static checks only | problems grouped by check (`json`, `imports`, `manifest`) |
| Inertia | `site/data/cockpit.json` (`inertia.flags`, `warnings`) | directions with many handoff sections since the registry last gained a record in them; the cockpit's build date. A `warnings` string counts as one warning; warnings that are not a list, or a threshold or streak that is not a whole number, make the section not available |
| Possible duplicates | the corpus index (`tools/corpus/duplicates.py` `near_duplicates`) | pairs at TF-IDF cosine 0.8 or above that involve a negative added in the window |
| Commands | nothing (static) | `been-tried`, the DQI screener, `baselines`, preflight and `check-new`, each with when to run it |

`agent_brief.json` holds every section in full. The markdown caps each list and table at 40
entries and then says how many more there are and where (`agent_brief.json`; for the referee,
`REFEREE_QUEUE.md` too). Text from the sources is kept verbatim on one line: a pipe stays a
pipe in list items (`|A|+|B|`), and in table cells it is escaped as `\|`.

**Degradation rule.** Every section returns `{"available": bool, ...}`. A section whose file
is missing, whose tool is not in the checkout, or that raises for any reason becomes
`{"available": false, "reason": ...}` and the page prints `Not available: <reason>` under its
heading. Not available never means "nothing to report", and one broken source never stops the
others. The registry section is unavailable, not "no change", when there is no git, on a
shallow clone, when the root is not the top of its own work tree, when no commit before the
window changed the registry, when the registry did not exist in that commit (it was deleted
there), or when git cannot read it there (a partial clone without that version); the
duplicates section is then unavailable too.

**Git.** Read-only, through an allow-list in the cockpit's style: exactly
`log -1 --first-parent --before=YYYY-MM-DDTHH:MM:59Z --format=%H<US>%ct -- research/registry/negative_results.json`,
`show <full sha>:research/registry/negative_results.json`,
`ls-tree --name-only <full sha> -- research/registry/negative_results.json` (only after `show`
fails, to tell a registry absent from that commit from one git cannot read) and
`rev-parse --is-shallow-repository --show-prefix`; anything else raises before git starts.
Git runs offline and never prompts: `GIT_NO_LAZY_FETCH=1` stops a partial clone fetching the
old registry from its remote (git 2.44 and later), `GIT_TERMINAL_PROMPT=0` stops a credential
prompt, stdin is closed, and a command that runs past 60 s makes the section unavailable.
Git always reads `--root`'s own repository: variables such as `GIT_DIR`, `GIT_WORK_TREE` and
`GIT_INDEX_FILE` (git exports them to hooks, and a shell may export them) are not passed on, so
a root that is not a checkout says so instead of being compared with another repository's history.
The baseline is the registry as the checked-out branch had it at the cutoff: its last change
before the window on the branch's first-parent line, each merge compared with the branch's own
side of it. So a record merged in from another branch during the window counts as added (and
one dropped by such a merge as removed), however old its commit on the other branch; and the
other branch never stands in for this one, whether it is a tool branch merged with `--no-ff`
that left the registry alone or a branch that changed the registry too. Run it on main for the
agents' view: on a branch that merges main in, main's registry changes count from the day they
were merged into that branch. The limit is the last second before the cutoff day (00:00 local
time, in UTC: `2026-10-12T12:59:59Z` for 2026-10-13 at UTC+11:00) because `--before` keeps a
commit dated exactly at its limit,
and it names a time because git reads a bare date (`--before=2026-10-12`) as that day at the
current time of day, so the same command picked a different commit in the morning and in the
evening. A shallow clone is refused outright: its oldest commit is a cut, so the commit before
the cutoff can be missing and an older one would be used without warning. So is a root below
the top of a work tree (a copy under `scratch/`, say): git would answer with the outer
repository's history and registry.

**Preflight's git.** All of the above is the brief's own git. The preflight section calls
`tools/preflight/preflight.py` `run()`, which runs its own git outside this allow-list,
environment and timeout: `git rev-parse --show-prefix --absolute-git-dir`, `git ls-files -z` and
`git diff-files --name-only -z --diff-filter=A`, the last two over `theorems/`, `core/` and
`qsearch_cli/`. They read the local index and work tree, never write the index and never
contact a remote; they are the commands preflight runs before every commit.

**Duplicates threshold.** 0.8, not the 0.9 of the committed registry report: the brief only
compares the window's new records, so the list stays short, and the corpus README's hand check
has a true restatement at 0.80. The nearest pair below it among the records of the ten days to
2026-10-21 is `NEG-ORTHOGONAL-PARABOLIC-DEQUANTIZATION-BOUND` / `NEG-UNITARY-...` at 0.773,
which the hand check classes as distinct. The corpus index is opened only when something was
added.

## Speed

Measured on this checkout on 2026-10-21:

| Run | Time |
|---|---|
| Default 7-day window (nothing added, so no corpus) | 5.2 s wall, 2.1 s CPU; the preflight section (its JSON parse of `research/classical_baselines/`) is 4.8 s of it |
| 10-day window (33 negatives added), corpus index already built | 11.4 s wall; the duplicates section 4.4 s, almost all of it the index refresh |
| 10-day window in a fresh worktree with no index | 31.5 s wall; building the lexical index took 26 s |

Again on 2026-10-22, after preflight began following the CLI's imports transitively (1092
modules), on a machine under heavy load (load average 150): the default window took 3.0 to
4.7 s wall and 2.2 to 2.5 s CPU over three runs, and later up to 16 s wall as the load grew.
The preflight section is still almost all of it: in-process, its JSON parse took 1.3 to 2.0 s
and its import walk 1.2 to 1.8 s. A 10-day window (19 negatives added) took 14.7 s in a fresh
worktree, building the index included, and 12.9 s with it built.

The index lives in the git-ignored `research/corpus_index/`. In the main checkout it already
exists, and the corpus MCP server keeps it current.

## First run (2026-10-21, before the referee passes)

- Registry: 975 records; 987 at 291e035d (2026-10-12). Nothing added; 12 removed, all now quarantined.
- arXiv watch: no open flags; the 22 flags first seen 2026-10-18 and 2026-10-19 all have verdicts
  (should-cite 9, related-only 8, false-alarm 5); 9 actions open (2610.06753 and 2610.03566 are done).
- Referee: not available (no `research/audits/reviews/reviews.json` yet).
- Preflight: 1 problem, the broken hypothesis contract (`Invalid \escape: line 7 column 167`).
- Inertia: four directions flagged in the cockpit of 2026-10-19 (OPI 13, BPQM 13, DCP 32, Ternary/lattice 22).
- Possible duplicates: no negative added in the window.

Tests: `python -m pytest -q tests/tools/test_brief.py`.
