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

It exits 0 whatever it finds; a `--root` that is not a directory or a `--since-days` below 1
is a usage error (exit 2). The window runs from 00:00 UTC on the day `--since-days` before
today (default 7).

## Why it exists

The agents are good at proposing and weak at checking, and the checks that exist sit in files
nothing reads at the start of a session: 22 flagged arXiv papers got human verdicts whose
actions are addressed to the agents (`research/audits/arxiv_verdicts.json`), the referee's
flags live in `REFEREE_QUEUE.md`, the cockpit's inertia flags in `site/data/cockpit.json`, and
preflight only helps when someone runs it. The brief puts each of them on one page.

## Sections

| Section | Reads | Shows |
|---|---|---|
| Registry | `research/registry/negative_results.json` in the working copy and at its last change before the window (git) | ids added and removed; removed ids now in `quarantined_campaign_negatives.json` are named as quarantined |
| arXiv watch | `research/audits/arxiv_collisions.json`, `research/audits/arxiv_verdicts.json` (via `tools/arxiv_watch/verdicts.py`) | possible kills and scoops with no verdict (however old), flagged papers first seen in the window with their verdict, verdicts recorded in the window, and every verdict action not marked `action_done` |
| Referee | `tools/referee/referee.py` `status()` over `research/audits/reviews/reviews.json` | notes flagged unsound or needs-work with their worst claim, and stale reviews |
| Preflight | `tools/preflight/preflight.py` `run()`, the static checks only | problems grouped by check (`json`, `imports`, `manifest`) |
| Inertia | `site/data/cockpit.json` (`inertia.flags`, `warnings`) | directions with many handoff sections since the registry last gained a record in them; the cockpit's build date |
| Possible duplicates | the corpus index (`tools/corpus/duplicates.py` `near_duplicates`) | pairs at TF-IDF cosine 0.8 or above that involve a negative added in the window |
| Commands | nothing (static) | `been-tried`, the DQI screener, `baselines`, preflight and `check-new`, each with when to run it |

`agent_brief.json` holds every section in full; the markdown caps each list at 40 entries.

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
`log -1 --before=YYYY-MM-DDT23:59:59Z --format=%H<US>%ct -- research/registry/negative_results.json`,
`show <full sha>:research/registry/negative_results.json`,
`ls-tree --name-only <full sha> -- research/registry/negative_results.json` (only after `show`
fails, to tell a registry absent from that commit from one git cannot read) and
`rev-parse --is-shallow-repository --show-prefix`; anything else raises before git starts.
Git runs offline and never prompts: `GIT_NO_LAZY_FETCH=1` stops a partial clone fetching the
old registry from its remote (git 2.44 and later), `GIT_TERMINAL_PROMPT=0` stops a credential
prompt, stdin is closed, and a command that runs past 60 s makes the section unavailable.
The baseline is the registry's last change before the window, not the last commit: the
path-limited log follows, at each merge, the parent whose registry the merge kept, so a tool
branch merged with `--no-ff` whose last commit falls just before the cutoff (and whose registry
is older than main's) cannot stand in for the registry as it was. The limit is the last second
before the cutoff day (00:00 UTC) because `--before` keeps a commit dated exactly at its limit,
and it names a time because git reads a bare date (`--before=2026-10-12`) as that day at the
current time of day, so the same command picked a different commit in the morning and in the
evening. A shallow clone is refused outright: its oldest commit is a cut, so the commit before
the cutoff can be missing and an older one would be used without warning. So is a root below
the top of a work tree (a copy under `scratch/`, say): git would answer with the outer
repository's history and registry.

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
