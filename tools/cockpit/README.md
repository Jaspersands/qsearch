# Agent cockpit

One page that answers "what have the research agents been doing?" from the
repository alone. `build_cockpit.py` reads the handoff log, the registry, git
history and the working tree, and writes `site/data/cockpit.json`.
`cockpit.html` (with `site/js/cockpit.js`) draws it.

## Build

From the repository root:

```
python tools/cockpit/build_cockpit.py                # writes site/data/cockpit.json
python tools/cockpit/build_cockpit.py --inertia 6    # flag a direction after 6 sections instead of 8
python tools/cockpit/build_cockpit.py --no-history   # skip the old versions of the handoff and registry (faster)
python tools/cockpit/build_cockpit.py --out /tmp/cockpit.json
```

A full build takes about 14 seconds. Most of that is reading about 100 committed
versions each of the handoff and the registry, six `git show` calls at a time.

With `--no-history`, sections stay undated and in file order, quoted ids are
credited from the current text, and registry growth and inertia are not
computed. The page says so. Commits, metrics and the working tree are still
read.

**Git use.** The builder runs git only with these exact argument lists:

- `rev-parse --is-shallow-repository`
- `status --porcelain --untracked-files=all`
- `log` with the builder's fixed formats: all commits with `--name-only`;
  commits touching the handoff, the registry, and the progress snapshot; and
  the last commit touching the checkpoint.
- `show <full sha>:<path>`, where the path is the handoff, the registry or the
  progress snapshot.

Any other argument list raises before git starts, including one carrying
`--output` or `-o`. The builder never imports `core/` or `theorems/`. Git output
and every file it reads are decoded as UTF-8, with bad bytes replaced.

Tests: `python -m pytest -q tests/tools/test_cockpit.py` (fixture handoff and a
fake git, no live repo) and `node --test tests/js/cockpit.test.mjs`.

## Dates, the head commit and warnings

- **Dates.** All dates are UTC days, taken from each commit's timestamp
  (`%ct`).
- **Build-time figures.** The page states its build date. Every figure that
  depends on it says so: "files uncommitted when this page was built",
  "commits in the 7 days to DATE", "days from the last checkpoint session to
  DATE".
- **Head commit.** "Head" is the commit the build started from. The commit that
  carries the page comes after it.
- **Missing git.** When git is missing, the page shows a warning at the top,
  and commits, dates, inertia, the working tree and the checkpoint's commit read
  "unknown" rather than "none".
- **Shallow clones.** In a shallow clone the page shows a warning, and sections
  are not dated from the truncated history. Commit counts and metrics cover only
  the fetched commits.
- **Load and draw errors.** If the data cannot be loaded, the page says so. If
  one panel fails to draw, that panel shows an error and the rest still draw.

## What each panel shows

- **Figures.** These are:
  - files uncommitted at build time
  - commits in the 7 days to the build date
  - directions flagged for inertia
  - handoff sections read
  - days from the last checkpoint session to the build date
- **Inertia.** For each research direction: how many of its own handoff
  sections were first committed after the last day the registry gained a
  record in that direction. See below.
- **Handoff log in order.** One tick per handoff section, oldest on the left,
  with one row per direction and one row per agent. The x axis is section
  order, not calendar time: a busy day takes many ticks and a quiet week none.
  Month labels show where each month's sections start. Orange ticks are
  sections first committed on a day the registry gained a record in their
  direction.
- **Latest handoff sections.** Newest first, filterable by direction and agent.
  It shows the cues behind each agent guess and the registry ids each section
  quoted first (see below). Each heading links to its line in the handoff *at
  the head commit* (`blob/<sha>/research/AGENT_HANDOFF.md`), so the links do not
  drift when `main` moves. A section that is not in the head commit gets no
  link.
- **Commits per day.** Every commit reachable from `HEAD`, by UTC commit day.
  Hover a day for its topics. There is also a topic table (last 14 days and
  all time) and the latest commits.
- **Research metrics.** The `metrics` block of every committed version of
  `research/progress_snapshot.json`, keyed by its `updated_at` date. When
  several versions share a date, the latest one is kept. Each metric gets its
  own small chart with a zero baseline.
- **Working tree.** Totals only: changed tracked files, untracked files, and
  their sum, from `git status` in the checkout that ran the builder. No file or
  folder names are published. The panel is labelled "when this page was built
  (DATE), before it was committed". It counts edits by every session using that
  checkout, not just the agents.
- **Research checkpoint.** "Checkpoint" here means `.research_checkpoint.json`
  at the repository root. It holds the session date, active milestone, latest
  verified subsystem, verified-subsystem count and scientific review status.
  The panel adds when the file was last committed, how many commits have landed
  since, and whether it has local edits ("unknown" without git). No code in the
  repository reads this file, so the panel reports what the agents last wrote
  down. It does not say whether the work is current.
- **Compute spend.** Shown only when `research/audits/spend_summary.json`
  exists. The section stays hidden when the file is missing. A malformed file
  is skipped with a warning on the page.
  - **Shape:** `{"generated_on", "days": [{"date", "runs", "wall_seconds",
    "cpu_seconds", "negatives_added", "tokens"}]}`, plus an optional
    `tokens_uncached`.
  - **Runs** are experiment runs only.
  - **Wall and CPU time.** A day with no timed command shows "not recorded" for
    both. Such a day has a null `cpu_seconds`, even though its wall time is
    written as 0.
  - **Tokens.** The token total says on how many days tokens were recorded,
    counted from the data ("on 71 of 76 days"). It includes cached input. The
    summary has no cached-token field; if days carry `tokens_uncached`, the page
    shows the cached share instead.

## Directions: the keyword table

Each `## ` section of `research/AGENT_HANDOFF.md` gets one direction. Scoring
works like this:

- 3 points for each distinct keyword in the heading.
- 1 point for each keyword mention in the body, with the body capped at 12.
- The highest score wins.
- Ties go to the direction listed first. The order puts narrow directions
  before broad ones.
- A section that scores nothing is **Other**.
- A win with under 3 points, or on a tie, is marked "weak match".

**Code fences.** Headings inside code fences are ignored. Both fence styles
count: ```` ``` ```` and `~~~`, three or more characters. A fence closes at a
line made only of the same character, at least as long as the opener. A fence
with no closer ends at the next `## ` heading, so a stray fence cannot swallow
the rest of the log.

Matching ignores case. It uses letter boundaries rather than word boundaries,
so `dcp_native_tree.py` and `dcp-native-tree` count as DCP while `HDQI` never
counts as `DQI`. In the table, a space also matches `-` and `_`.

| Direction | Keywords |
|---|---|
| HDQI | hdqi, hamiltonian dqi |
| OPI / prime character | opi, dqi, prime character, morse, jacobi, optimal polynomial intersection, known norm, norm solver/attack/witness, reed solomon, semicircle |
| BPQM / polar | bpqm, polar code/source/conditional/shaping/sampler, successive cancellation, belief propagation, gibbs |
| DCP / dihedral coset | dcp, edcp, dihedral, dhs, dhsp, hidden shift, subset sum, kuperberg, regev, sine window, phase bank |
| Carrier / PGM | carrier(s), pgm, pretty good measurement, racah, plancherel, recoupling, involution, hyperoctahedral, tetrahedral, 6j, naimark, selector(s) |
| Ternary / lattice | ternary, trit(s), lattice(s), lwe, rlwe, ring lwe, cvp, svp, usvp, lll, babai, ntru, dgs, cyclotomic, q-ary, sis, pip, principal ideal |
| Code equivalence | code equivalence, self dual, goppa, quasi cyclic, hull, support splitting, permutation code, wreath |

**Measured coverage** on the real handoff (494 sections, built 2026-10-19):

| Direction | Sections |
|---|---|
| DCP / dihedral coset | 118 |
| Ternary / lattice | 113 |
| Carrier / PGM | 103 |
| Code equivalence | 88 |
| OPI / prime character | 13 |
| BPQM / polar | 13 |
| HDQI | 2 |
| Other | 44 (8.9%) |

96 of the 450 classified sections are weak matches. The first version of the
table used word boundaries and required 2 points. That left 34.4% as Other,
because snake_case module names and single mentions did not count.

Commits use the same table, more strictly. The subject decides when it names a
direction. Otherwise the changed paths decide, but only when every path
keyword points to the same direction. As of 2026-10-19, 152 of 213 commits
(about 71%) are Other. Most of those are site and tooling work, or large
"wire N modules" commits that touch many directions at once.

Registry records use the same table too. See "Registry growth" below.

## Agents: attribution from wording

Every commit has the same human author, so git cannot tell the agents apart.
The handoff policy section ("Objective And Operating Policy") says Codex does
the high-reasoning work and Gemini (via Antigravity) the mechanical work. The
two write differently:

| Codex | Gemini |
|---|---|
| Says "No GPT commit/push" or "GPT next" (explicit) | Headings like "Investigation 12 Proved" (explicit) |
| Talks about Gemini in the third person: "Gemini can…", "remains Gemini work" (explicit) | "Antigravity … Completion Note" headings (explicit) |
| "Current High-Reasoning Result" headings | Em dashes and ampersands in headings, "Proved" in headings |
| "Files and experiment ID:" template | Heavy **bold**, inline LaTeX `$…$` |
| Numerals glued to words ("in48.66s", "at110") | Stock phrases: "strictly enforced", "100% COMPLETE", "fully wired" |
| CAPS emphasis (NOT, SAME, ALL, ONLY…) | Long unwrapped lines (a quarter or more of prose lines over 100 characters) |
| Prose hard-wrapped at about 80 characters | |

Each cue adds points to one side (weights are in `CUES` in the builder). A
section gets a label only with at least 3 points and a lead of at least 2.
Otherwise it is **unknown**.

**Result:** 327 Codex, 56 Gemini, 111 unknown.

**Check.** 283 sections name their author outright, through the explicit cues
above. With those cues removed, the style cues alone agree with the named
author on 143, disagree on 0 and abstain on 140. So the labels it does give
look reliable. It abstains a lot, mostly on older sections written in a plain
hard-wrapped style with no self-reference.

**Limits:**

- The two Gemini agents write alike, so there is a single "gemini" label. The
  builder does not try to separate them.
- A section edited by both agents gets whichever style dominates.
- These are wording habits. An agent that changes its style will be mislabeled
  or left unknown.

## Registry growth

Growth is read from the git history of
`research/registry/negative_results.json`, not from the handoff:

- **Baseline.** The first committed version that parses is the baseline.
- **Gains.** A record is a gain on the UTC day of the first later version that
  contains its id.
- **Later moves.** A gain stays counted even if the record is later moved to
  the quarantine file or removed.
- **Uncommitted records.** Records present only in the working tree count as
  "uncommitted" gains, after every committed section.

Each gained record gets a direction from the keyword table. Its id is scored as
the heading, and its claim and `applies_to` tags as the body. A record that
matches no keyword is **unclassified**. It counts toward growth but ends no
direction's run.

**Measured on 2026-10-19:**

- **Versions.** 105 committed versions.
- **Baseline.** 2026-07-15, with 464 records.
- **Gains.** 528 records gained, the last on 2026-10-12, and none uncommitted.
  Of the 528, 11 were later moved to quarantine. 5 baseline records were later
  removed. That leaves today's 987 ids.
- **By direction.**

  | Direction | Records |
  |---|---|
  | Code equivalence | 276 |
  | Carrier / PGM | 101 |
  | DCP / dihedral coset | 44 |
  | Ternary / lattice | 2 |
  | OPI, BPQM, HDQI | 0 |
  | Unclassified | 105 (19.9%) |

- **Weak matches.** 49 of the classified records are weak matches.

## Inertia

Sections are walked oldest first. For each direction, the **streak** is the
number of its own sections first committed after the last day on which the
registry gained a record in that direction.

- **Gain days.** Sections first committed on a gain day are not counted, and
  they end a run. Days are the finest grain that both histories share.
- **Other directions.** Sections about other directions neither count nor end
  a run.
- **Late gains.** A gain after a direction's last section gives a streak of 0.
- **Flags.** A direction is flagged when its streak reaches the threshold
  (`--inertia`, default 8). Other is a catch-all and never flagged.
- **Earlier runs.** The page also lists earlier runs that reached the
  threshold, with the gain day that ended each one.

On 2026-10-19 at threshold 8, four directions are flagged:

- OPI (13): no record in this direction since the baseline.
- BPQM (13): no record in this direction since the baseline.
- DCP (32): last gain 2026-10-12, 3 records.
- Ternary / lattice (22): last gain 2026-10-12, 1 record.

**What changed.** Inertia used to count sections since one first quoted a
registry id. Only 72 of the 528 gained records are ever quoted, so long runs
hid real growth. Checked against the registry history above, the old runs
contained gains in their own direction:

| Old run | Sections | Dates | Gains inside the run |
|---|---|---|---|
| Code equivalence | 84 | 2026-08-06 to 09-08 | 267 code-equivalence gains |
| Carrier / PGM | 57 | 2026-08-06 to 09-08 | 54 |
| Carrier / PGM | 11 | 2026-09-08 to 09-11 | 43 |
| DCP | 70 | 2026-09-17 to 10-09 | 11 |

None of the 9 current runs contains a gain in its direction.
`test_no_reported_run_spans_a_day_on_which_its_direction_gained_a_record` checks
the same property on the fixture.

DCP rose from 12 to 32. The old rule was reset by a 2026-10-18 DCP section
quoting an ergodicity id. That record had been added on 2026-10-12 and first
quoted by the Investigation 49 section.

**Read flags with care:**

- **A flag measures the registry, not effort.** It says the registry stopped
  gaining records in that direction. Work that ends in a correction, a positive
  result or a module with no registry record does not end a run.
- **Classification errors.** The direction of a record comes from keywords.
  The 105 unclassified records end no run, and a misfiled record ends the wrong
  one.
- **Day grain.** Day grain hides order within a day. A section committed hours
  after a gain on the same day is not counted.
- **Directions with no gains.** OPI and BPQM have gained nothing since the
  baseline, so their streak is every section they have.
- **Quiet directions.** A direction that has gone quiet keeps its last streak.
  The "Latest section" column shows how long ago that was.

## Quoted registry ids

The sections table has a column "Registry ids first quoted here". This is the
quoted-id signal, kept as a label only; inertia does not use it.

**Matching.** A token counts only when it is exactly a real registry id. Real
ids are those in today's registry, the quarantine file, or any committed
registry version. Tokens are runs of letters, digits and `_` joined by one or
more hyphens, so `NEG-A--B` matches whole, and `NEG-A-B-v2` does not count as
`NEG-A-B`. An id broken across a line at a hyphen is joined.

**Credit from history.** Each id is credited to the section that held it in the
first committed handoff version that quotes it. Within that version, a section
new in that version wins, then the lowest (oldest) one. Ids quoted only in
uncommitted text are credited from the current text.

**Measured on 2026-10-19:**

- 71 ids are credited from history and 0 from the current text.
- 1 id (`NEG-SYMMETRIC-GROUP-KRONECKER-RACAH-BARRIER`) is lost: the section that
  first quoted it is no longer in the handoff.

## Dating sections

Handoff sections carry no reliable dates. Only about a quarter have a date in
the heading. Instead, each section is dated by the first commit of the handoff
file whose version contains its heading. Two refinements:

- Status prefixes such as "Latest:", "Prior:" and "Current:" are stripped
  before matching, so a renamed status keeps its date.
- Repeated headings are matched by occurrence, counting from the bottom.

Sections first committed on the same day keep their file order: lower in the
file counts as older. Uncommitted sections count as newest.

**Limit:** a heading that was reworded after its first commit looks newer than
it is. With `--no-history`, sections are in file order and undated.
