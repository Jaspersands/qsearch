# Note referee

An independent, adversarial read of the research notes marked review pending. Most notes
in `research/*.md` say "REVIEW PENDING" and nobody outside the agent that wrote them has
checked them. The referee hands each note to a fresh in-session judge, which picks the
claims that carry the conclusion, quotes each one from the note, and says whether it
holds, has a gap, is wrong or is unclear. The tool checks every quote and keeps the
reviews in one file, keyed by the note's content hash so a review goes stale when the
note changes.

The referee never edits `research/*.md`. Its outputs go to `research/audits/`.

```bash
python tools/referee/referee.py select [--prefix PRIME] [--limit 30] [--include-reviewed] [--json]
python tools/referee/referee.py export --out-dir DIR [--limit 30] [--prefix P] [--batch-size 5]
python tools/referee/referee.py export --out-dir DIR --note PRIME_CHARACTER_OPI --note POLAR_SOURCE_DESIGN
python tools/referee/referee.py import DIR/out/*.jsonl --judge claude-subagent-2026-10-21
python tools/referee/referee.py render
python tools/referee/referee.py status [--json]
```

| Command | What it does |
|---|---|
| `select` | Lists review-pending notes, newest first, without a current review. |
| `export` | Writes `INSTRUCTIONS.md` and `batch_NN.json` (five note packets each) for the judges. `--note STEM` (repeatable) exports exactly those notes whatever their status; the name's letter case must match. Exit 2, nothing written, when `--out-dir` is a file or already holds `batch_*.json` from an earlier export (use a new folder per pass). |
| `import` | Checks judge rows and stores them in `reviews.json`. Exit 2, nothing stored, when a file cannot be read or a row fails. A `stem` must be a note name (letters, digits, `_`, `.`, `-`), never a path, spelled as the file is, letter case included (macOS would open `BAR_NOTE.md` for `bar_note`). |
| `render` | Writes one `reviews/<STEM>.md` per review and `REFEREE_QUEUE.md`. |
| `status` | Flagged (unsound or needs-work) reviews whose note is unchanged, and stale ones. Used by the agent brief. |

## Selection

A note is review pending when the corpus status rule (`note_status` in
`tools/corpus/sources/markdown.py`) says so: the first eight lines, title excluded, match
"review pending" and nothing more decisive (quarantined, superseded, retracted,
rejected). Notes that say "require review" instead are `unlabelled`, so export them with
`--note`. The two journals (`AGENT_HANDOFF.md`, `MECHANICAL_FOLLOW_UP_PLAN.md`) are never
selected. Notes are ordered by the first date in the status block (the first paragraph
after the title), undated last, then by stem. File modification times are not used: they
follow checkout and copy order, so every checkout of one commit gets the same queue and
the same cut at `--limit`. A note whose stored review has its current content hash is
skipped unless `--include-reviewed` is given.

## The packet

`build_packet` gives the judge the full note `text` plus fields parsed from it
(`extract.py`):

- `date`, `status`, and `not_claimed`: preamble sentences or bullets containing "not" or
  "no".
- `producer`: the note's own `python theorems/<stem in lower case>.py <flags>` when the
  note runs it, else the first `python theorems/<module>.py <flags>` anywhere in the note.
  A note that runs no command but has a stem script `theorems/<stem in lower case>.py`
  gets that script with `command: null`. The JSON `artifact` is an `x/y.json` path in the
  note named after the script, else the script's own `REPORT = "...json"` constant (a
  line starting `REPORT =` or `REPORT: ... =`, never `BASE_REPORT`) when that file exists,
  else the first `x/y.json` path in the note, else `REPORT`. Paths resolve against the
  repository root, then against `research/`.
- `result`: the first section whose heading contains Result, Question, Claim or Summary
  and not Not, Cannot, Why, Next ... Question or Kill/Break ... Claim ("What Can And
  Cannot Be Claimed" is not a result), else the first section. `derivations`
  (Derivation, Lemma, Proof, Bound, Bounds, Bounding, Certificate or a numbered heading;
  not Bounded or Boundary), `controls` (Controls, Comparison, Classical) and `self_check`
  (the first of Prove ... Wrong, Disprove, Falsifier, Falsification, to/and/can Falsify,
  Refutation, Attempt To Break, Kill, Self-Critique, Red Team) come from the headings
  too. `decision` is the first heading with Decision or Next, passing over a result
  heading ("Question And Decision") and a "Why ..." motivation when another one exists.
  Headings inside fenced code are not section breaks.
- `flags`: the flags the claim checker (`tools/claim_checker/check.py`) raises on the
  result's prose. Flags it marks negated ("No membership oracle is supplied") are left
  out, since the note rules them out.
- `artifact_excerpt`: the artifact's top-level keys, then its numeric and short string
  leaves, lists capped at five items, at most 4000 characters. Leaves are taken in turn
  from each top-level key (depth first within a key) and printed grouped by key, so a
  large first key does not crowd out the others.
- `artifact_path`: where the artifact actually is, relative to the repository root, or
  null. Notes often write `x/y.json` for `research/x/y.json`.
- `content_sha`: SHA-256 of the note's bytes.

These fields are pointers, not a summary: the heading rules take the first match, so a
note whose headings use other words gets an empty or misleading field (a note's own
algorithm under "Classical ..." lands in `controls`), and a note that only runs other
modules gets the first of them as its producer. The judge is told to work from the full
text.

## The judge loop

1. `export --out-dir research/audits/reviews/<pass>` writes the instructions and batches.
2. One fresh general-purpose subagent per batch reads `INSTRUCTIONS.md` and its
   `batch_NN.json`, and writes `out/batch_NN.jsonl`: one row per note with `stem`,
   `content_sha`, `overall` (`sound`, `needs-work`, `unsound`, `unclear`), `summary` and
   up to six `claims`, each with a verbatim `quote`, a `verdict` (`holds`, `gap`, `wrong`,
   `unclear`), the `step` at fault, a `finding` (the counterexample or missing condition)
   and `covered_by_self_check`. The judge must not propose new research.
3. `import out/*.jsonl --judge NAME` rejects the whole file on an unknown verdict, a
   `covered_by_self_check` that is not `true` or `false` (omitted or null reads as false),
   more than six claims, an `overall` that contradicts the claims (the worst claim sets it:
   `wrong` requires `unsound`, else `gap` requires `needs-work`, else `unclear` requires
   `unclear`, and claims that all hold require `sound`; a row with no claims may be `sound`
   or `unclear`), a quote under six words, or a quote that is not in the note text (all
   claims are checked). A quote's words (runs
   of letters and digits in any script, so Greek variables and superscript exponents count;
   an underscore splits words) must appear consecutively in the note after lower-casing,
   and the symbols between them, before the first and after the last (`<`, `>`, `=`, `+`,
   `-`, `/`, `^`, `~`, `±`, `√`, decimal points; `≤` and `<=` count as the same, and so do
   `-`, `−`, `–` and a run of them) must be the note's, so `b>=epsilon` does not pass for
   `b<=epsilon`, nor `>= min(1, ...)` for `<= min(1, ...)`. A prose em dash (`—`) may be
   written `-` or left out. List and quote markers at the note's line starts may be kept or
   dropped, but a kept marker must be the note's. The stored quote is the note's own
   wording of the span, not the judge's copy, widened to whole whitespace-delimited tokens
   (less a trailing `.`, `,`, `;` or `:`) so that a sign or operator next to the first or
   last word is kept. A quote lifted from the artifact excerpt fails, because
   it is not in the note. A `content_sha` must be 64 lower-case hex digits. A row whose
   `content_sha` differs from the note's current hash (the note was edited after export)
   is stored with `stale: true`, and its quotes are checked against the text the judge
   read, taken from the `batch_NN.json` beside the judge file (in its folder or the folder
   above) when that text's hash matches. When packets for the note sit beside the judge
   file but none of them has the row's `content_sha`, the sha was miscopied and the file
   is rejected. Only when no exported packet for the note is found is a quote that is not
   in the current note stored as the judge wrote it with `verified: false` instead of
   rejecting the file. Two rows for one note in one import (one file or several) reject
   the import. Re-importing a note replaces its review, except that a row that is stale
   on arrival (an earlier pass imported again) never replaces a stored review of the
   note's current bytes: import keeps that review and reports the row as skipped. Stored
   text is capped: summary 1500 characters, finding 600, step 300, quote 400.
4. `render` rebuilds the per-note reviews and the queue.

Cost: about 100k tokens per batch of five notes.

## Outputs

- `research/audits/reviews/reviews.json`: `{"notes": {STEM: {reviewed_on, judge,
  content_sha, overall, claims, summary, stale}}}`, sorted. Each claim has `quote`,
  `verified`, `verdict`, `step`, `finding` and `covered_by_self_check`. Import writes it to
  a temporary file and renames that over it, so it is never left half written. When it
  cannot be read or lacks that shape (each entry an object, its claims objects with a
  string `quote` and `verdict`), every command stops with a one-line error naming the file
  and exit 2, and import leaves it as it is.
- `research/audits/reviews/<STEM>.md`: the overall verdict, summary and each claim with its
  quote, verdict, step and finding; marked stale when the note changed since.
- `research/audits/REFEREE_QUEUE.md`: counts by overall verdict (current reviews) and
  stale, flagged notes with their worst claim (wrong, then gap, then unclear), stale
  reviews, and the next 30 unreviewed review-pending notes.

A review is one model's reading of one note. It is a triage for the agents and the
human, not peer review: a `holds` means the judge found no gap, not that the claim is
proved.

## Calibration

On 2026-10-21 the referee (`tools/referee`) ran three times, independently, on one batch of four review-pending notes behind the classical-competitors preprint: `PRIME_CHARACTER_OPI`, `PRIME_CHARACTER_NORM_ATTACK`, `POLAR_SOURCE_DESIGN` and `POLAR_CONDITIONAL_SAMPLER`. The packets are in `research/audits/reviews/calibration/batch_01.json`, and judges A, B and C wrote to `out/`, `out_repeat_b/` and `out_repeat_c/`. Their output was compared with the preprint's review history (`docs/papers/classical-competitors/README.md`, three passes on 2026-10-19).

### Verdicts

| Note | A | B | C |
| --- | --- | --- | --- |
| PRIME_CHARACTER_OPI | needs-work | needs-work | needs-work |
| PRIME_CHARACTER_NORM_ATTACK | needs-work | sound | sound |
| POLAR_SOURCE_DESIGN | sound | needs-work | sound |
| POLAR_CONDITIONAL_SAMPLER | sound | sound | sound |

No judge returned wrong or unsound. Pairwise agreement on overall verdicts is A–B 2/4, A–C 3/4 and B–C 3/4, and every split comes from a single gap raised by one judge. Each judge checked 24 claims. Every number any judge compared with an artifact matched. C could not check the OPI live numbers because the packet's artifact path does not resolve (see below).

### Known findings against the judges

Grading: **yes** means the judge raised it as a gap or wrong claim. **partly** means the judge checked the underlying fact but did not flag it. **no** means the judge did not touch it. **n/a** means the finding is about the preprint's wording or about a note outside this batch.

| Review-history finding | Note | A | B | C | Evidence |
| --- | --- | --- | --- | --- | --- |
| N=31, K=16 mixed seed-71 input stops at 30/31 (second pass) | OPI / NORM_ATTACK | partly | partly | no | The OPI note reports "31/29 to31/30". NORM_ATTACK lists only the N127 mixed controls as left over and says nothing about N31,K16, where its budget K>max(\|A\|,D) can never hold. A and B matched 31/30 against the artifact and went no further. C never checked it. |
| Polar certificate presented as unconditional; rests on two review-pending derivations (second pass) | POLAR_SOURCE_DESIGN | no | partly | no | The note says it "removes the missing public-set construction premise", and the sampler note's header says "resolves" it, while the conditions sit only at lines 3–4 and 176. B flagged that sentence, but for scope rather than dependence. A and C re-derived both derivations, found them sound, and said nothing about the conditionality. The packet status for both polar notes was `unlabelled`. |
| Omitted conditioning on the syndrome in Result C (must-fix) | preprint only | n/a | n/a | n/a | The sampler note states E_s TV(Q_s, P(U\|U_F=s)) ≤ 2ε_F explicitly, and all three judges verified it. The error came in at drafting. |
| Fixed-input guarantee stated too broadly (must-fix) | preprint only | n/a | n/a | n/a | The OPI and NORM_ATTACK headers scope it correctly. The guarantee comes from the Morse note, which is not in this batch. Only C restated the per-instance limit. |
| "PPT bound equals collective"; three Result B bounds rounded the wrong way; Result B rounded to nearest | preprint only | n/a | n/a | n/a | Result B, not in this batch. |
| Wrong reason for the zero bounds; "only above" a threshold; N = 15 controls ignored; 169/756-bit field sizes | preprint only | n/a | n/a | n/a | The Morse and exterior-bound notes, not in this batch. |
| Mis-scoped "best classical witness" | preprint only | n/a | n/a | n/a | The OPI note already says "not certified local optima". |
| Korada–Urbanke covers only the joint step; "Lemma 2"; Virmani pages; a new citation's clause | preprint only | n/a | n/a | n/a | Citations. The judges did reconstruct the joint-then-conditional split. |
| "Highest share" audit sentence; audit section update; Reproducibility claim; reproduce.sh claim; conventions, tolerance, r = 4 prime, angle formula, spacing, bibliography | preprint only | n/a | n/a | n/a | These are preprint text, tooling and bibliography items. |
| Seventh must-fix (the README counts 7 and names 6) | preprint only | n/a | n/a | n/a | It is not named in the README, so it cannot be mapped. |

Of the four findings that matter most for this calibration, two turned out to be preprint drafting errors over correctly scoped notes: the syndrome conditioning and the fixed-input breadth. The other two have note-level roots, and **no judge raised either one**.

### Findings the review history does not contain

| Note | Judges | Finding | Check |
| --- | --- | --- | --- |
| OPI | A, B, C | The p5, N4, K2 tight-degree strict counterexample does not state the coset orientation. | **Real, minor.** A brute force over F5 gives 0 perfect strict polynomials at K2 for a square β but 1 for a nonsquare β (Q=3). The test uses `global`, which means orientation 0. The note needs "square common coset" added. |
| NORM_ATTACK | A (B and C disagree) | The "at least 1/(2N)" corollary fails at N=1. | **Doubtful.** N=1 with D=2 needs K≥3>N, which is outside an RS code of length N. With K≤N the bound holds. At most the note should state K≤N. |
| POLAR_SOURCE_DESIGN | B | One certified length (N32768) is called a half-rate "family". | **Real, in wording.** Every coarse half-rate design from N16 to N4096 fails, and the premise needs ε_F→0. The preprint keeps "For this polar family …" (main.tex line 239). |
| POLAR_SOURCE_DESIGN | A | The N1024, 361-constraint Gibbs sample exists only in the tests. | **Real, provenance only.** The artifact's N1024 row has no samples. `tests/test_polar_source_design.py:151-160` runs the sample. |
| OPI | A, B, C | The artifact path `classical_baselines/prime_character_opi.json` does not resolve. | **The path problem is real; C's "not in the repository" is wrong.** The file is under `research/`, and the numbers C marked unclear match it. |
| NORM_ATTACK | B | The artifact stores seeds 1038/1080, not 29/71. | **Real, trivial.** The producer uses seed+1009. |

### What the referee missed

- It raised neither note-level finding from the review history. On N31 it matched the score and moved on. It did not notice that NORM_ATTACK's decision paragraph leaves the N31,K16 mixed controls out, or that its degree budget cannot apply there.
- It did not flag the polar notes' headline sentences ("removes"/"resolves the missing public-set premise"), which drop the review-pending conditions the same notes state elsewhere.
- Neither the referee nor the review history noted that the OPI note reports only the common-coset results for r=3 (N63,K46) and r=4 (N32,K24). The artifact's mixed scores there are 55 and 56 of 63, and 28 and 27 of 32.
- Packet defects weakened the run:
  - The OPI artifact path lacks `research/`.
  - Both polar notes have status `unlabelled`.
  - OPI has `self_check: null`.
  - Every packet has an empty `derivations`.
  - The NORM_ATTACK `not_claimed` list contains a sentence about the Morse solver.

### What this says about using the referee

- It works as an independent check of derivations and numbers. All three runs found the same real OPI defect, re-derived every load-bearing argument, and matched every number they checked.
- A finding raised by only one run is a lead, not a verdict. Of the two such findings here, one is real and one is doubtful. Use at least two runs, and verify any finding raised by only one.
- It reviews notes in isolation. It cannot catch what a preprint adds at drafting, and 19 of the 21 mapped review items were of that kind. It is no substitute for a check of the preprint against its notes.
- It judges whether each quoted claim follows. It does not check what a note leaves out of its summaries, or whether a headline sentence keeps the note's own conditions, and it missed both note-level findings for those reasons. The packet builder should fix the defects above before the next run.

### Round two (revised instructions)

Round two changed two things in `INSTRUCTIONS.md`. The packet gained an `artifact_path` field, and the instructions added two checks: the scope of headline sentences (title, status, result and decision must keep the review-pending derivations, the sizes actually certified and the inputs where the method fails) and omissions in summaries (a summary of cases must match every case the note or artifact reports). Two fresh judges, D and E, reviewed the same four notes (`research/audits/reviews/calibration_r2/`).

| Finding | A | B | C | D | E |
|---|---|---|---|---|---|
| N31,K16 mixed seed-71 (30/31) left out of NORM_ATTACK's decision; degree budget cannot hold (review history) | no | no | no | yes | yes |
| Polar headlines ("removes" / "resolves the premise") drop the review-pending derivations (review history) | no | no | no | yes | yes |
| OPI p=5 counterexample needs the square coset | yes | yes | yes | yes | yes |
| One certified length (N32768) called a family | no | yes | no | yes | yes |
| NORM_ATTACK 1/(2N) fails at N=1 (false positive: the degree budget excludes N=1) | yes | no | no | no | no |

- Both judges found both review-history findings that round one missed. They also kept every real round-one finding and dropped A's N=1 false positive, which they correctly rated holds.
- New, checked as real: neither OPI's open-case list nor NORM_ATTACK's decision mentions the unsolved r=3 N63,K46 (55, 56/63) and r=4 N32,K24 (28, 27/32) mixed inputs, and OPI never reports their scores. NORM_ATTACK also says common cosets were "solved", but the K39 global inputs score 108/127 and 110/127.
- With `artifact_path`, both judges checked the OPI repair totals, which C could not find in round one.
- The new checks also produced three low-value gaps: a table without the N16 row (D), the NORM_ATTACK title (E), and an unnamed fully solved configuration (E). Treat a scope gap with no effect on a conclusion as minor.
- Both judges rated all four notes needs-work. This batch has no correctly scoped note, so whether the new checks over-flag clean notes is still untested. The next calibration should include one.

The four calibration notes' stored reviews are round-two judge D's.

## First pass (2026-10-21)

`research/audits/reviews/pass1/` holds the first pass over the 30 newest review-pending
notes, made with the revised instructions. Each batch of five went to two independent
judges (`out_a/`, `out_b/`). A third agent then checked, against the note, its artifact and
small recomputations, every claim either judge marked gap, wrong or unclear and every claim
on which they disagreed. It dropped what it could not confirm and wrote the stored review
(`out/`).

| Overall | Notes |
|---|---|
| needs-work | 25 |
| sound | 5 |
| unsound or unclear | 0 |

The two judges gave the same overall verdict for 25 of the 30 notes, and both rated four
notes sound, so the new scope checks do not flag every note (the open question left by
round two of the calibration). Most gaps are
headline-scope gaps: a title, status line or decision sentence that drops a condition the
body states (review pending, the sizes actually certified, the inputs where the method
fails). Read those as wording fixes unless the finding says a conclusion changes. No claim
was found wrong, so the plan's hand spot-check of two unsound claims had nothing to check;
the reconciling agent's per-claim checks took its place.
