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
| `export` | Writes `INSTRUCTIONS.md` and `batch_NN.json` (five note packets each) for the judges. `--note STEM` (repeatable) exports exactly those notes whatever their status. |
| `import` | Checks judge rows and stores them in `reviews.json`. Exit 2, nothing stored, when a file cannot be read or a row fails. A `stem` must be a note name (letters, digits, `_`, `.`, `-`), never a path. |
| `render` | Writes one `reviews/<STEM>.md` per review and `REFEREE_QUEUE.md`. |
| `status` | Flagged (unsound or needs-work) reviews whose note is unchanged, and stale ones. Used by the agent brief. |

## Selection

A note is review pending when the corpus status rule (`note_status` in
`tools/corpus/sources/markdown.py`) says so: the first eight lines, title excluded, match
"review pending" and nothing more decisive (quarantined, superseded, retracted,
rejected). Notes that say "require review" instead are `unlabelled`, so export them with
`--note`. The two journals (`AGENT_HANDOFF.md`, `MECHANICAL_FOLLOW_UP_PLAN.md`) are never
selected. Notes are ordered by the first date in the status block (the first paragraph
after the title), undated last, then by file modification time. A note whose stored
review has its current content hash is skipped unless `--include-reviewed` is given.

## The packet

`build_packet` gives the judge the full note `text` plus fields parsed from it
(`extract.py`):

- `date`, `status`, and `not_claimed`: preamble sentences or bullets containing "not" or
  "no".
- `producer`: the note's own `python theorems/<stem in lower case>.py <flags>` when the
  note runs it, else the first `python theorems/<module>.py <flags>` anywhere in the note,
  with its JSON `artifact`: an `x/y.json` path in the note named after the script, else
  the `REPORT = "...json"` constant in the script's source when that file exists, else
  the first `x/y.json` path in the note, else `REPORT`. Paths resolve against the
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
3. `import out/*.jsonl --judge NAME` rejects the whole file on an unknown verdict, an
   `overall` that contradicts the claims (a `wrong` claim requires `unsound` and
   `unsound` requires a `wrong` claim; a `gap` with nothing wrong requires `needs-work`),
   a quote under six words, or a quote that is not in the note text. A quote's words must appear
   consecutively in the note after lower-casing (what the rediscovery audit's `_norm`
   keeps, matched on word boundaries), and the symbols between them (`<`, `>`, `=`, `+`,
   `-`, `/`, `^`, `~`, decimal points; `≤` and `<=` count as the same) must be the
   note's, so `b>=epsilon` does not pass for `b<=epsilon`. List and quote markers at line
   starts may be kept or dropped. The stored quote is the note's own wording of the
   span, not the judge's copy. A quote lifted from the artifact excerpt fails, because
   it is not in the note. A row whose `content_sha` differs from the note's current hash
   (the note was edited after export) is stored with `stale: true`, and its quotes are
   checked against the text the judge read, taken from the `batch_NN.json` beside the
   judge file (in its folder or the folder above) when that text's hash matches. When no
   exported text is found, a quote that is not in the current note is stored as the judge
   wrote it with `verified: false` instead of rejecting the file. Re-importing a note
   replaces its review. Stored text is capped: summary 1500 characters, finding 600,
   quote 400, six claims.
4. `render` rebuilds the per-note reviews and the queue.

Cost: about 100k tokens per batch of five notes.

## Outputs

- `research/audits/reviews/reviews.json`: `{"notes": {STEM: {reviewed_on, judge,
  content_sha, overall, claims, summary, stale}}}`, sorted. Each claim has `quote`,
  `verified`, `verdict`, `step`, `finding` and `covered_by_self_check`.
- `research/audits/reviews/<STEM>.md`: the overall verdict, summary and each claim with its
  quote, verdict, step and finding; marked stale when the note changed since.
- `research/audits/REFEREE_QUEUE.md`: counts by overall verdict (current reviews) and
  stale, flagged notes with their worst claim (wrong, then gap, then unclear), stale
  reviews, and the next 30 unreviewed review-pending notes.

A review is one model's reading of one note. It is a triage for the agents and the
human, not peer review: a `holds` means the judge found no gap, not that the claim is
proved.
