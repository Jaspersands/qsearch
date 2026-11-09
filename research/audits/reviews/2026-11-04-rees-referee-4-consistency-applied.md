# Rees paper, referee pass 4 (consistency): fixes applied (2026-11-04)

Source: `research/audits/reviews/2026-11-04-rees-referee-4-consistency.md`.
Edited: `docs/papers/rees-hsp/main.tex` and the six `appendix-*.tex` files.
Backup of the pre-edit `.tex` files:
`/private/tmp/claude-501/-Users-jaspersands-Developer-qsearch/6a6cfdd7-c9d4-4169-9805-7e18625bbdd7/scratchpad/bak-i171/`.
This was done by an AI session. It is not a human review. Nothing was
committed. Not touched: `docs/outreach/`, `research/reductions/*.json`, any
code, `make_numbers.py`, `numbers.tex`, `formal/README.md` and
`docs/papers/rees-hsp/README.md`.

Each claim was checked against the source before its fix was applied. The
checks are listed per item.

## Result

| | Applied | Applied-modified | Skipped |
|---|---|---|---|
| Error (8) | E1, E2, E3, E4, E6 | E5, E7, E8 | none |
| Gap (13) | G2, G3, G7, G8, G9, G10, G11, G12 | G1, G4, G5, G6 | G13 |
| Imprecision (13) | I1, I2, I3, I4, I5, I6, I11, I12, I13 | I7, I8, I10 | I9 |
| Style (6) | S2, S3, S4 | S1, S5, S6 (item 3 skipped) | none |
| **Total (40)** | **25** | **13** | **2** |

Build: every `*.tex` file and `references.bib` were copied to the scratchpad
`build/` folder, and `latexmk -pdf -interaction=nonstopmode main.tex` ran
with exit code 0. The log has 0 "Overfull", 0 "Float too large", no
undefined or multiply defined references or citations, and no `!` errors.
BibTeX gave no warnings. The output is **135 pages**.
`tests/tools/test_rees_paper_numbers.py` gave **2 passed**. No `\begingroup`
or `\mathrel` was added.

## Errors

- **E1 (applied).** S38 and S39 were replaced by the referee's text, which
  is now the new `\paragraph{Scope.}`. Check: S33 gives the class-four
  coherent backend "3330 exact transforms", and S10 gives the fifth backend
  "230 exact transforms". So the explicit-transform bound covers only the
  third backend and `rees_circuit_full.py` (S12 and S18).
- **E2 (applied).** S22 was replaced by the referee's text. The removed
  parenthetical said which backend uses which lemma. S8 and S10 still say
  that, so no content is lost. Check: at κ=1, Lemma `lem:coherent-linear-sde`
  says its column count is g+1.
- **E3 (applied).** In `appendix-schedule2.tex`, κ ≥ 7 became κ ≥ 8. Check:
  the same list, and `main.tex`, give E_2(7) exactly.
- **E4 (applied).** Check: `theorems/rees_circuit_general.py:82` imports
  `is_sde_solve` and calls it at line 1321. `theorems/rees_end_to_end_ext.py:68`
  imports it. The arith, qft-wire and coherent backends reach it through
  `rees_circuit_general`.
- **E5 (applied-modified), `appendix-subspace.tex` and `main.tex`.**
  - Kept "quantum implementation" for the preparer (growth instrument).
  - Added "at arities other than those of Schedule~1". The subspace core is
    defined with Schedule 1, but the circuits run at Chevalley–Warning or
    coherent arities. Without this, the replacement sentence would itself be
    imprecise.
  - The pointer reads "the paragraphs from Gate-level control to Scope",
    because the paragraph is now split.
- **E6 (applied), `rem:tb-compiler`.** Check: `main.tex` (black-box
  pullback) says "now takes an annihilating modulus". The report
  `2026-11-02-rees-prime-power-compiler.md` §6 lists six test points,
  (3,2,2), (5,3,4), (7,2,5), (11,2,5), (7,2,6) and (11,2,6), so c ≤ 6.
- **E7 (applied-modified).**
  - Dropped the referee's "only" from "only the coherent-label circuits ...
    run at that arity". Remark `rem:fc-tradeoff`(a) in
    `appendix-free-coordinate.tex` also runs rounds of the triangular
    construction.
  - So the parenthetical now ends "and Remark~\ref{rem:fc-tradeoff}(a) uses
    its rounds".
- **E8 (applied-modified).** Changed "1--2" to "1--4" November and added the
  three items the referee lists. "The gate counts of the Gate-level control
  paragraph" became "of the paragraphs from Gate-level control to Scope"
  (split). Table `tab:fcs-budget` and the sets E_2(κ) were already in the
  list.

## Gaps

- **G1 (applied-modified).** The inserted sentence says "the circuits for
  κ_d ≥ 2 run at the arity of Proposition triangular-sde". The referee had
  "these circuits", but the κ_d = 1 circuit runs at g+1. The clause after it
  now starts its own sentence: "The circuit of this lemma is wired only into
  ...". Check: p ∈ E_2(p−1) for p ≥ 5 (appendix-schedule2 scope list).
- **G2 (applied)** at both places. Check: Thm `thm:uniform-compilation`(iii)
  cites Kitaev and points to Lemma `lem:qft-mod`.
- **G3 (applied).** The items were merged into the existing list: "..., the
  running time of every solver and of the whole algorithm, Lemma qft-mod,
  ... ; no formally checked compiler is claimed."
- **G4 (applied-modified).** Check: no report records a build of
  `Formal/Audit.lean` after the 21 guards were added. The `lean-c5` report
  ran `lake build` only on the three new modules. The
  `referee-3-body-applied` report, item 6, notes the same open point. The
  `.lake` timestamps suggest a build ran: `Audit.olean` is from 13:10:48,
  after `Audit.lean` at 13:10:29.
  - So I did not write "the guards themselves have not been built", which
    may be false.
  - Instead the text adds: "no report records a build of
    \file{Formal/Audit.lean} after that addition".
- **G5 (applied-modified).** The reason comes from
  `2026-11-04-rees-circuit-coherent-c4.md` §3.7. The ninth subgroup,
  γ_2 = ⟨e3, e4, e5⟩, was not run because its conditioned state needs about
  16 GB.
- **G6 (applied-modified).** The three headers now say "proof sketch,
  counts checked against the generated gate lists; AI-checked, pending human
  review". The coherent-sde, -k2 and -k3 reports check the closed forms
  against the emitted gate lists, so "counts from the gate lists" was not
  exact. "Conditional on Proposition triangular-sde" was added to
  `lem:coherent-power-sde`, as proposed. It was also added to
  `lem:coherent-quadratic-sde`, which runs the same proposition. Both are
  extra caveats.
- **G7, G8, G9, G10 (applied).** For G8, the bibliography has no Shor or AKS
  key, so the text names them without citing.
- **G11 (applied).** `Rabin1980` is in `references.bib`. The text had
  "Rabin" only in source comments. The sentence comes after
  `\end{lemma}` of `lem:s3-root`.
- **G12 (applied).** "AI-checked, pending human review" was added to the
  headers of `prop:single-evaluation`, `prop:refresh` and `prop:conjugation`.
  All three are proved in the paper.
- **G13 (skipped).** The fix is optional. Its clause "does not change the
  stated exponents" would need a recount of how many inversions every gate
  bound in `prop:tb-count-gates` uses. That is a new claim I could not
  verify, so (H2) stays a hypothesis.

## Imprecisions

- **I1 (applied)** through the split. S11 now begins "For the third backend,
  by a hybrid argument ...".
- **I2, I3, I4 (applied).** For I4: `lem:coherent-power-sde` does not
  define m.
- **I5 (applied).** The four primes of the table with p ≥ 5184 are 5281,
  2^31−1, 2^61−1 and 2^127−1. All four are among the six primes of (b).
- **I6 (applied).** Check: `2026-11-02-rees-small-prime-arity.md` gives the
  proven ranges up to 2441 and 3583. `dfs2-prune` line 120 says dfs2 started
  at 2442.
- **I7 (applied-modified)**, in `main.tex` and in `appendix-schedule2.tex`.
  The text now reads "and shows 10321 ∈ E_2(8) and, by a separate run,
  17659 ∈ E_2(9)". 10321 lies inside the decided range. 17659 comes from
  the chunk file `dfs2b_k9_17501_20000.out`.
- **I8 (applied-modified).** Changed in four places. The referee gave no
  wording for "It was run twice, independently", so I used "separately".
  - The rendered text has no other "independent" that describes an AI check.
  - The source comments (subspace:24, free-coordinate:13) were left as they
    are.
- **I9 (skipped).** It concerns `docs/papers/rees-hsp/README.md`, which is
  outside the `.tex` scope of this task. The integrator should note that the
  README also says "Independent automated referee passes", the I8 wording.
- **I10 (applied-modified).** Added "for odd p", because Lemma `lem:qft-mod`
  needs odd N.
- **I11 (applied).** The body now states the appendix bound
  poly(m, log 1/ε) for queries. Appendix-codimension (ii) and its proof
  (lines 284 and 311–315) derive exactly this. It is the proved bound, not a
  new claim, but the integrator may want to confirm.
- **I12 (applied).** Check: B_d(a) = G(d,a)^⌈log₂(d+1)⌉ with
  G = d^{d(d−1)/2}(a+1)^d. So its degree in a is d⌈log₂(d+1)⌉.
- **I13 (applied).** Check: Lemma `lem:tb-count-exponent` gives
  E_W(2..4) = 5, 11, 23.

## Style

- **S1 (applied-modified): Gate-level split.**
  - The paragraph now has five parts:
    - Gate-level control: S0–S2, S20–S21, E2, I2, S24–S26.
    - Binary arithmetic and explicit transforms: S3–S7, then S11–S15.
    - Coherent-label backends: S8, S9, S10, the class-four sentence,
      S34–S37, then S16–S19.
    - Instances: S27–S32 and the first half of S33.
    - Scope: E1.
  - The opening "A coherent-label version of these class-four circuits"
    would point forward, so it became "of the class-four circuits over
    $\mathbb{F}_7$ of the Instances paragraph".
  - "below" became "of the Instances paragraph" in S5 and S12. S5 also gained
    the missing comma. S8 contained no "below".
  - A script check found that 30 of the 40 original sentences appear
    verbatim. The other 10 were replaced as listed.
  - Every number of the old paragraph still appears in the new text, with
    the same or higher multiplicity, so none is missing. New numbers come
    only from the E1, E2, I3 and G5 text.
- **S2 (applied).** $m$, $g$, $e$ and $\rho$ were added to the notation
  list.
- **S3 (applied).** The text reads "the final round $k$ ... $-e_{k+1}$". In
  the stop round, R = e_{k+1} + v_{k+1} and v_{k+1} = 0.
- **S4 (applied).** Both places now cite `app:s2-scope`.
- **S5 (applied-modified).**
  - "II call" became "Imran--Ivanyos call".
  - The doubled comma was fixed.
  - Trappeniers is now cited by `\cite[...]{Trappeniers2024}`. Kitaev is
    handled by I10.
  - The second "checked directly" became "For the listed witnesses:".
  - (H2) and (H3) now each have their own sentence. (H1) stays in the
    sentence that says it holds by Lemma `lem:qft-mod`.
- **S6 (items 1–2 applied, item 3 skipped).**
  - Items 1–2: the stale comments in `appendix-torsion-blackbox.tex` were
    updated.
  - Item 3 was skipped. The comments in `appendix-schedule3.tex` and
    `appendix-free-coordinate.tex` that say "B <= 7 + ..." correctly record
    what the scripts checked: `fc_appendix_check.py:90` asserts
    `B <= 7 + (u-1)*clog2(4u)`. Changing them to 6 would misreport the
    check. The bound 6 + ... is stated and proved in the text.

## For the integrator

1. **G4.** Run `lake build --wfail` in `formal/` and recount the guards. If
   the build passes, the sentence can say so.
2. **G13.** Decide whether to keep (H2) as a hypothesis. Settling it needs
   an inversion count across `prop:tb-count-gates`.
3. **I9.** Decide on `docs/papers/rees-hsp/README.md`: its 2 November
   status, the "365 guards" figure, the "Independent automated referee
   passes" wording and the "inputs each one only if it exists" sentence.
4. **I11.** Confirm the body's query bound now matches the appendix.
5. **G1, G3, G6.** New caveat sentences were added. Check that they read
   well.


## Integrator follow-up (11-04 ~17:45)

- G4: integrator ran `~/.elan/bin/lake build Formal.Audit` in `formal/`: "Build completed successfully (3490 jobs)." `Formal/Audit.lean` has 455 `#print axioms` lines. main.tex sentence updated to record the build.
- I11: confirmed against appendix-codimension Prop. app-codim-birthday (Q = t a B, poly(m, log 1/eps) for fixed k).
- G13: (H2) stays a hypothesis.
- I9: paper README updated by the integrator (see integration log I171).
