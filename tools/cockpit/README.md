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
python tools/cockpit/build_cockpit.py --no-history   # skip dating sections from git history (faster)
python tools/cockpit/build_cockpit.py --out /tmp/cockpit.json
```

A full build takes about 7 seconds. Most of that is reading the 100-odd
committed versions of the handoff file. Git is only ever asked to `log`, `show`
and `status`. The builder refuses any other git command, and it never imports
`core/` or `theorems/`.

Tests: `python -m pytest -q tests/tools/test_cockpit.py` (fixture handoff and a
fake git, no live repo) and `node --test tests/js/cockpit.test.mjs`.

## What each panel shows

- **Figures.** Uncommitted files, commits in the last 7 days, directions
  flagged for inertia, handoff sections read, and days since the last
  checkpoint session.
- **Inertia.** For each research direction: how many of its own handoff
  sections have passed since one added a new registry entry. A direction is
  flagged once that count reaches the threshold (default 8).
- **Handoff log over time.** One tick per handoff section, oldest on the left,
  with one row per direction and one row per agent. Orange ticks are sections
  that added a new registry entry. The x axis is section order, not calendar
  time. Month labels show where each month's sections start.
- **Latest handoff sections.** Newest first, filterable by direction and agent.
  It shows the cues behind each agent guess and links each heading to its line
  in the handoff.
- **Commits per day.** Every commit reachable from `HEAD`, by commit date. Hover
  a day for its topics. There is also a topic table (last 14 days and all
  time) and the latest commits.
- **Research metrics.** The `metrics` block of every committed version of
  `research/progress_snapshot.json`, keyed by its `updated_at` date. When
  several versions share a date, the latest one is kept. Each metric gets its
  own small chart with a zero baseline.
- **Working tree.** `git status --porcelain --untracked-files=all` in the
  checkout that ran the builder. It counts changed tracked files and untracked
  files, by top-level folder. It is read before the builder writes its output,
  and file names are not published.
- **Research checkpoint.** "Checkpoint" here means `.research_checkpoint.json`
  at the repository root. It holds the session date, active milestone, latest
  verified subsystem, verified-subsystem count and scientific review status.
  The panel adds when the file was last committed, how many commits have landed
  since, and whether it has local edits. No code in the repository reads this
  file, so the panel reports what the agents last wrote down. It does not say
  whether the work is current.
- **Compute spend.** Shown only when `research/audits/spend_summary.json`
  exists (shape: `{"generated_on", "days": [{"date", "runs", "wall_seconds",
  "cpu_seconds", "negatives_added", "tokens"}]}`). The section stays hidden when
  the file is missing. A malformed file is skipped with a warning on the page.

## Directions: the keyword table

Each `## ` section of `research/AGENT_HANDOFF.md` gets one direction. Headings
inside code fences are ignored. Scoring works like this:

- 3 points for each distinct keyword in the heading.
- 1 point for each keyword mention in the body, with the body capped at 12.
- The highest score wins.
- Ties go to the direction listed first. The order puts narrow directions
  before broad ones.
- A section that scores nothing is **Other**.
- A win with under 3 points, or on a tie, is marked "weak match".

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
keyword points to the same direction. As of 2026-10-19, 143 of 203 commits
(about 70%) are Other. Most of those are site and tooling work, or large
"wire N modules" commits that touch many directions at once.

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

## Inertia and what counts as a "new registry entry"

A **new registry entry** is an id that meets two conditions:

- It appears in `research/registry/negative_results.json` or
  `research/registry/quarantined_campaign_negatives.json`. Any prefix counts:
  NEG-, CODE-, COSET-, and so on. Ids split across a line break are joined.
- A handoff section mentions it, and no older section did.

Sections are walked oldest first. For each direction, the **streak** is the
number of that direction's own sections since its last section with a new
entry. Sections about other directions in between neither count nor reset it.
A direction is flagged when its streak reaches the threshold (`--inertia`,
default 8). Other is a catch-all and never flagged. The page also lists
earlier runs that reached the threshold.

On 2026-10-19 at threshold 8, four directions are flagged:

- OPI (13)
- BPQM (13)
- DCP (12)
- Ternary / lattice (22)

**Read flags with care:**

- Codex sections routinely state "no central candidate/negative/proof
  promotion" and rarely quote registry ids. A long Codex streak can therefore
  mean "working without registering", not "stuck".
- The registry gained no new ids after 2026-10-12. Its later history only
  removes ids.
- A direction that has gone quiet keeps its last streak until it is mentioned
  again. The "Latest section" column shows how long ago that was.

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
