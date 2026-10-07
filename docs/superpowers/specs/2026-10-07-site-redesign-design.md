# Q-Search website redesign — design spec

Date: 2026-10-07
Status: approved in brainstorming, pending spec review

## Goal

Replace the current "academic monograph" site with a light, plain, genuinely useful
site that a general technical visitor (portfolio audience) can understand in one
read, and that a skeptical expert can verify. It must not look AI-generated.

## Decisions

| Question | Decision |
| --- | --- |
| Primary audience | Portfolio / general technical visitors; experts are the secondary audience |
| Simulated widgets (Falsifier Arena, in-browser pytest, Spectral Sandbox) | Removed. All interactivity uses real registry data |
| Page structure | 4 pages: Home, Open problems, Negative results, How it works. Old URLs redirect |
| Look | White, typographic, restrained. Explicit anti-slop rules below |

## Problems being fixed

- Three stacked navigation bars (publication banner, header, 12-link section rail).
- 10,600 px homepage with 13 sections that repeat the same four candidates.
- Every section uses the same eyebrow + serif H2 + grey paragraph + bordered card pattern.
- Sub-pages use unstyled browser-default tables; IDs wrap across 3–4 lines.
- Mobile: Falsifier cards overflow horizontally, pipeline SVG unreadable, header wraps to 3 rows.
- Spectral Sandbox default state ("c = +1.00 (Standard)") reports 3 collisions, contradicting Theorem 1. Its eigenvalues are hand-typed.
- "Run in Browser" prints PASSED for `tests/test_fourier_decay.py`, `test_commutant.py`, `test_dhs_sieve.py`, `test_code_syzygy.py` — none exist. `-k "smoke"` selects zero tests.
- Fabricated or overstated labels: "ISSN 2026-QSRCH", "Peer-Verifiable", "100% Deterministic", "guaranteeing zero unchecked claims".
- Hardcoded counts (914) disagree with the snapshot (929). "&zap;" renders literally.

## Visual system

### Anti-slop rules (hard constraints)

1. No eyebrow labels above headings. No all-caps monospace micro-labels.
2. No grids of identical icon/number/title/tag cards.
3. No pills or badges except the single status marker (rule 8).
4. No shadows, gradients, glows, pulses, holographic effects, drop caps, or fake terminal chrome.
5. Rounded containers only where a control needs one (inputs, buttons). Structure comes from type, whitespace, and hairline rules.
6. Copy is plain and first-person plural. Banned words: monograph, protocol APG, rigorous, first-class, certified, peer-verifiable, deterministic audit, executive abstract, laboratory.
7. Every number on the page comes from data, carries a date, and links to its source file.
8. Status vocabulary is exactly three terms — **open**, **ruled out**, **active** — rendered as a small colored dot plus plain text, identical on every page. Mapping: a track with snapshot tone `active` is **active**, any other track is **open** (its current route failed, but the problem is unresolved); frontiers and proof debts are **open**; negative results are **ruled out** (implied by the page, so rows carry no marker).

### Tokens

- Page `#FFFFFF`; text `#111111`; secondary text `#555555`; muted `#767676` (AA on white); hairline `#E6E6E6`.
- One accent, muted red-orange (`#C2410C` range, tuned for AA contrast on white), used only for status and the current verdict.
- Links: underlined, text-colored; hover darkens the underline.
- Typefaces (Google Fonts): Schibsted Grotesk for headings and UI; Source Serif 4 for long prose; JetBrains Mono only for literal paths and commands. Tabular figures for numbers.
- Layout: prose measure ~66ch; wide content (tables, chart) up to ~1100px. On desktop, a right-hand margin column holds sources, dates, and file links beside the claim they support (Tufte-style). Below ~900px margin notes fold inline beneath their paragraph.

## Pages

Shared header on every page: wordmark "Q-Search", links Home · Open problems · Negative results · How it works, and GitHub. Shared footer: last-updated date, GitHub, citation link.

### Home (`index.html`)

1. **Intro** — one plain paragraph on what the project is; current verdict with date; three figures (ideas ruled out, experiments run, open proof debts) with a margin note linking each to its source JSON.
2. **Where things stand** — the snapshot's tracks as rows: name, status marker, one-line summary, next step. A row expands to show `evidence` and `summary`.
3. **Activity** — one SVG chart: experiment runs per week (bars, from `site/data/activity.json`) with the negative-results total over time (line, from the `metrics.negative_results` value in each `site/data/changelog.json` entry). Run statuses are free-form strings, so the line is not derived from runs.
4. **Results so far** — snapshot `milestones` as a short list; KaTeX where it helps.
5. **What changed** — changelog of verdict and track-status changes over time from `site/data/changelog.json`.
6. **Check it yourself / cite** — commands that work (`python qsearch.py validate`, real test files under `tests/`), copy buttons, BibTeX with counts filled from data.
7. **About** — `execution_model` text from the snapshot plus one short authorship line.

### Open problems (`open-problems.html`)

- Ranked frontiers from `research/frontier_map.json`: priority, id, why it matters, next experiment; kill criteria collapsed under each.
- Proof debts from `research/proof_debt_report.json` as a compact table grouped by `debt_type`; the shared `required_resolution` text becomes the group header rather than repeating per row. Filter by candidate.

### Negative results (`negative-results.html`)

- Search box and filter chips by `applies_to` tag with counts.
- Each record is one line (id + claim), expanding to reason invalid, lesson, evidence, and a GitHub link to `source` when it is a repo path.
- Each record has a permalink anchor (`#<id>`); loading a URL with a hash opens and scrolls to that record.
- Paginated or incrementally rendered so 929 records stay responsive.

### How it works (`how-it-works.html`)

- The loop (propose → classical attack → record → proof gate) as one simple inline SVG diagram.
- Plain definitions: proof debt, dequantization, negative result, kill criterion.
- Repository map: top-level folders → contents → GitHub links; main `qsearch.py` commands.
- Limits: numerical checks are not formal proofs; derivations marked review-pending; how and when research runs.

### Redirects

`methodology.html` and `repomap.html` → `how-it-works.html`; `frontier.html` and `proof-debt.html` → `open-problems.html`. Each is a minimal page with `<meta http-equiv="refresh">`, a canonical link, and a visible fallback link.

## Data and build

- Static site: HTML + one stylesheet (`site/styles.css`, rewritten) + small vanilla JS files under `site/`. No framework, no bundler. KaTeX is dropped: no page shows typeset math once the simulated widgets are gone. Chart drawn as hand-written SVG.
- `research/progress_snapshot.json` (existing `tools/build_progress_snapshot.py`) remains the source for verdict, tracks, milestones, metrics, conjecture, execution model.
- New `tools/build_site_data.py` (deterministic, no wall-clock time) writes:
  - `site/data/activity.json` — weekly run counts (ISO weeks, from `recorded_at`) from `research/experiment_run_history.json`.
  - `site/data/changelog.json` — one entry per distinct `git log` version of `research/progress_snapshot.json`: date, commit, verdict title, track statuses, metrics, and a list of what changed versus the previous entry. Generated locally and committed. `build_site_data.py --skip-changelog` regenerates only the git-independent files (used by CI, which has a shallow checkout).
  - `site/data/negatives.json` — `research/registry/negative_results.json` reduced to displayed fields.
- No counts hardcoded in HTML. Every test path and command shown on the site must exist / run.
- Failure handling: if a data file fails to load, the section shows one sentence and a link to the raw file on GitHub. No permanent "Loading…" states.

## Verification

- Headless (Playwright) screenshots of all 4 pages and 4 redirects at 1440 px and 390 px; reviewed manually. Automated assertions: no horizontal overflow (`scrollWidth <= innerWidth`), no console errors, redirects land on the right page.
- `tools/check_site.py`: every repo path referenced in site HTML/JS exists; displayed counts match their JSON sources.
- CI (`.github/workflows/validate.yml`): `node --check` on all `site/*.js`; run `tools/build_site_data.py --skip-changelog` and `git diff --exit-code` them; parse-check `changelog.json`; run `tools/check_site.py`.
- Manual review against the anti-slop rules before completion.

## Out of scope

Dark mode, README changes, any change to research code or registries, analytics, a JS framework.

## Revision 2026-10-07 b: circuit identity and negative-results map

After reviewing the first build, the user found it too plain and chose two concepts from a prototype page (`circuit as layout` and `map of where we looked`). The Fourier-sampling demo and phase coloring were rejected. Everything above still applies except where this section overrides it.

### Circuit as the home page's spine

- Three vertical wires run down the left gutter of the home page, one per snapshot track (labels from `short_title`).
- Five gates, in order: hypothesis, structure, classical attack, proof gate, separation. The first four sit beside the first four home sections (intro, where things stand, activity, results so far). The separation gate sits at the bottom of the circuit, above the footer, labelled "?".
- Wire ends are data-driven from each track's `stage` (integer) and `tone`:
  - tone other than `active`: the wire is solid down to gate `stage + 1` (capped at the proof gate) and ends there in a measurement symbol.
  - tone `active`: the wire is solid down to gate `stage` and continues dashed to the separation gate.
  - A gate box spans only the wires still alive at that gate.
- Scroll progress: the live part of each wire darkens and an accent dot rides the active wire. Disabled under `prefers-reduced-motion`.
- Gutter: 150 px on desktop, 60 px below 760 px.
- Other pages get a horizontal three-wire strip under the header using the same plan (ends and dashed continuation), as a compact progress map.

### Map at the top of Negative results

- `tools/build_negative_map.py` (local, needs scikit-learn) computes a 2D layout of all negative results: TF-IDF over id, claim, and reason → truncated SVD → t-SNE (fixed seed) → k-means regions labelled with the most distinctive two-word phrase from their claims. Output: `site/data/negative_map.json` with `points: [{id, x, y}]` normalised to [0, 1] and `regions: [{x, y, label, count}]`. Committed; CI only parse-checks it.
- The page draws the map on a canvas above the search box. Point color = track (the four filter tags plus grey for other). This is the one place the site uses colors beyond the single accent.
- Map and list are synced: points not matching the current search/filter are dimmed; clicking a point opens and scrolls to its record in the list on the same page (keeping the current filter if the record matches it). Hover shows id and claim.
- Records without map coordinates still appear in the list; a note states how many are not yet on the map.
- The home page's "ideas ruled out" figure links to the map.
