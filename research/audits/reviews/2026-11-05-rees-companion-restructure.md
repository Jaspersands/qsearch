# Rees HSP companion paper: restructure from project log to journal paper

Date: 2026-11-05. AI-only integrator pass (Claude Fable 5.1 with seven
helper agents), owner-approved ("restructure yes"). No human review. No git,
no network; `make_numbers.py` not run; `docs/outreach/` and
`research/reductions/rees_hsp_reduction.json` untouched; `core/main-core.tex`
not edited. Input: referee 14 (`2026-11-05-rees-referee-14-fable.md`, Style
S1, S3, S6 and the structural half of the summary) and its application record
(`-referee-14-applied.md`, "For the owner: structure"). The pre-restructure
state is archived unchanged in
`docs/papers/rees-hsp/archive/main-2026-11-05-before-restructure/`.

Files edited: `docs/papers/rees-hsp/main.tex` and all six existing
`appendix-*.tex`. Files created: `appendix-sde-side.tex`,
`appendix-backends.tex`, `appendix-filters.tex`, `appendix-provenance.tex`.
No label was renamed or removed; every `% NEEDS HUMAN VERIFICATION` comment is
kept (23); every theorem, lemma, proposition, corollary, definition, proof,
table, equation and numbers macro is kept (counts below). No claim changed
status; no speedup, novelty, human-review, implemented-receiver or general-SDE
claim was added.

## New outline (main.tex, 199 pp.; body pp. 5--63, appendices pp. 64--199)

Front matter: title, date, a one-paragraph **Status of this paper** (replaces
the 38-line dated status box), abstract, contents.

1. Introduction (background and non-gradability barrier; related work; core
   idea; input contract and main results with `thm:main`, `rem:main-solver`,
   `tab:main-regimes`, contributions, organization; notation and the
   status-label convention)
2. The Positive Lower-Central Rees Cover and the Tuple Lift (unchanged order)
3. The Complete Central Instrument (unchanged; finite controls kept as
   paragraphs, paths moved out)
4. All-Record Recursive Descent (quotient conversion; recursion, error budget,
   `lem:hybrid`; the proof of `thm:main` moved to Section 7)
5. Whole-Grade SDE Schedules (new section, from the former Subsection 4.3):
   5.1 Schedule 1 (`thm:is-import`, `rem:is-import`, shortened
   `rem:is-runtime`), 5.2 Schedule 2 (`thm:power-sde`, `prop:decoupled-sde`,
   shortened `rem:two-level-threshold-size`, `prop:triangular-sde`,
   `rem:triangular-scope`), 5.3 the combined rule, 5.4 Schedule 3
   (`thm:free-coordinate`)
6. Uniform Gate Compilation and Resource Bounds (`thm:uniform-compilation`,
   `lem:qft-mod`, one backend table `tab:backends` plus a 15-line paragraph in
   place of five backend-by-backend paragraphs, the coherent witness lemmas,
   `prop:coherent-receiver`, resource profiles)
7. Proof of the Main Theorem (new section; the proof paragraph and the "steps
   behind Theorem main" paragraph, verbatim, now after the schedules and the
   compilation, as in the core paper)
8. Classical Query Complexity (the former Subsection 8.1; `prop:classical-query`,
   `rem:query-separation`, `tab:query-crossover`)
9. Parameterized Regimes (unchanged content; de-logged)
10. Black-Box Groups and Flat Subspace Sources (`thm:bb-envelope`(iii)
    shortened to its exponents with a pointer to `prop:tb-count-gates`)
11. Mechanical Verification in Lean 4 (dated build chronology compressed to
    the facts; the "Reproducibility" subsection moved to Appendix J)

Appendices: A Schedule 2, B Schedule 3 (uniform kernel), C free-coordinate
schedule, D flat subspace source, E ring-to-field and black-box (with a new
`rem:tb-count-envelope` holding what `thm:bb-envelope`(iii) stated beyond
`prop:tb-count-gates`), F hidden codimension, **G Supplementary Results on
the Diagonal-Equation Solvers** (new: tape layout and run counts of the
Schedule 1 solver, `rem:sde-side-tape`; barriers for the two-level
threshold, `rem:sde-side-barrier` [argued]; `rem:sde-subquadratic`,
`rem:sde-block-steered`, `rem:sde-worst-case` moved here), **H Gate-Level
Circuit Backends** (new: the former backend prose), **I Classical Filters for
Natural Algebraic Actions** (new: the former Section 8 preamble, `rem:filters`
and the application searches), **J Provenance and Verification Record** (new:
reproduction paragraph, then 84 entries P1--P84 keyed by result label, each
with status, source report(s), check report(s), scripts and data; 373
repository paths).

## What moved where

- 220 `\file{}` occurrences in `main.tex` and 73 in the appendices (all 184+
  distinct paths the referee counted, plus those added since) left the running
  text. In the text each is now `(Appendix~\ref{app:provenance},
  item~\ref{prov:...})` or nothing where a status label suffices.
- Status box -> "Status of this paper" (front matter); its paths -> P1 (paper
  construction, change logs, referee reports) and the Lean entries.
- Proof of `thm:main` (Section 4.2 end) -> Section 7.
- Subsection 4.3 -> Section 5 with four subsections.
- `rem:is-runtime` tape layout and run-count constructions -> Appendix G.1.
- `rem:two-level-threshold-size`, "arguments made only in the cited reports"
  -> Appendix G.2 (`rem:sde-side-barrier`).
- `rem:sde-subquadratic`, `rem:sde-block-steered`, `rem:sde-worst-case`
  -> Appendix G.3 (labels unchanged).
- Five backend paragraphs of Section 5.1 -> `tab:backends` + Appendix H.
- "Reproducible Resource Profiles": artifact list -> P-entries; captions keep
  every number and status label.
- `thm:bb-envelope`(iii) 40-line item -> short item + `rem:tb-count-envelope`
  (Appendix E).
- Section 8 classical filters -> Appendix I; Subsection 8.1 -> Section 8.
- Section 9.2 "Reproducibility" -> Appendix J head.
- Appendix A 79-line integrator comment block -> 5 lines (comments).

## Project-log language removed

Dated notes (version history, "4--5 November", "on 2 November 2026"
-> "at the time of writing"), "pass"/"passes" of agents, "the parent",
"AI session(s)" -> "AI-checked", "owner decision" -> "we do not adopt it
here" / stated as adopted, "the previous version ... withdrawn" (13+8
passages): where the passage recorded a mathematical fact (why a direct
descent fails; why multiplying registers does not add characters; the
Davenport-constant existence statement) the mathematics stays as plain prose;
pure history was dropped and is listed per fragment under "Removed history"
in the scratchpad fragments (summarised: the omitted Dixmier--Lister bracket,
the pulled-back-subgroup FPT(k) claim, the arity 2d^3 g_d attribution, the
Omega(p^55) collision argument, the copy-only postselection route, the earlier
scalar-flag bound, the compiler version note, the Lean build chronology).
Numbers that depended on running scans (E_2(8), E_2(9) decided ranges 13873 /
16363) are now stated as "the search has not been completed beyond these
ranges" and may need refreshing.

## Checks

(a) Labels: archive 254, new 362 (108 new labels: sections, provenance items,
new appendix subsections and remarks); missing from archive: none; duplicate
labels: none.

(b) Status labels, archive -> new (comments excluded): "AI-checked, pending
human review" 136 -> 240; "finite computation" 53 -> 140; "argued" 6 -> 33;
"conditional" 103 -> 130; "machine-checked" 15 -> 28; "pending human review"
168 -> 279; `% NEEDS HUMAN VERIFICATION` 23 -> 23. Theorem-like environment
headers: 159 -> 162; every archive header that carried a status word has a
header in the new text with the same title and the same status words (three
headers retitled: `rem:sde-worst-case` semicolons reordered, label kept;
"Other project filters; conditional on the cited notes" -> "Other classical
filters; conditional on their sources"; "Relation to the source note and to
prior work" -> "Relation to prior work and to an alternative outer loop").
Environment counts archive = new: theorem 14, lemma 66, proposition 31,
corollary 10, definition 5, proof 119, equation 17, align 5; remark 37 -> 40
(three new remarks), table 13 -> 14 (`tab:backends`). numbers.tex macros in
use: 160 -> 160, none lost.

(c) `grep -c '\\file{'` is 0 in `main.tex` and in every appendix except
`appendix-provenance.tex` (373).

(d) `grep -E 'overnight|2026-11|pass |parent|session|I2[0-9][0-9]'` on the
text with comments stripped returns only mathematical uses: "chain-pass
scan/envelope" (main.tex, resource profiles), "forward pass", "finishing
pass", "once that pass is fixed" (Appendix G, the block-steered and
worst-case procedures), the tree "parent"/"parents" (Appendices B, C), "parent
queries" (P-entry for the codimension checks), and the dates inside file
paths in Appendix J. No dated note, agent pass, session, version note or
integration row remains in the text.

No new `\mathsf`, `\mathrel`, `\begingroup`, `\aa` or `\ni` (one `$K \ni 0$`
copied into a provenance entry was rewritten as `$0 \in K$`).

## Build and tests

Full paper (scratchpad copy, `latexmk -g -pdf`, `nice -n 19`): exit 0,
199 pages (archive: 183; the provenance appendix is 22 pages), 0 Overfull,
0 undefined references or citations, 0 multiply-defined labels, no "Float too
large". Core paper (`core/main-core.tex`, own copy): exit 0, 27 pages,
0 Overfull, 0 undefined.
`pytest -q tests/tools/test_rees_paper_numbers.py`: 2 passed.
`pytest -q tests/test_rees_circuit_round2.py -k "not slow"`: 20 passed,
1 skipped.

## Left for the owner

- Referee 14 S2 (14 unlabelled headers) and S8 (letter reuse in Appendices B
  and C) were not applied; the status-label convention is now stated once in
  the front matter and in Section 1.
- `docs/papers/rees-hsp/README.md` still describes the old file list; the
  four new appendix files are not listed there.
- The decided E_2(8)/E_2(9) ranges should be refreshed from the scan outputs
  before any release.

## Addendum (referee 19, 2026-11-05)

Referee 19 (`2026-11-05-rees-referee-19-companion.md`, Section 1(b) and
Style S2) notes that this record omits one change made after the
restructure: integration row I239 synchronised 9 companion statements with
the referee-18 core: `def:input-contract`, `thm:main`, `rem:main-solver`,
`rem:is-import`, `thm:uniform-compilation`, `lem:collision`,
`prop:classical-query` and `rem:query-separation` (the referee counts 9
changed statements and names these 8 labels; the I239 row lists the same
places). The referee compared each with the
current core statement: same content. No statement changed status. Two items
of "Left for the owner" are now done: `README.md` lists the four new
appendix files, and I239 refreshed the decided E_2(8)/E_2(9) ranges (16993
for kappa = 8, 16633 for kappa = 9; 20107 the largest proved member of
E_2(9); 1370 of the 1373 kappa = 9 sweep exceptions open). Referee-19
application record: `2026-11-05-rees-referee-19-applied.md`.
