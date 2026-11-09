# Referee 19 (companion pre-send check): application record

Date: 2026-11-05. AI-only (Claude Opus 5.5 subagent). No human review. No
git, no network; `make_numbers.py` not run (the numbers test only loads it);
`docs/outreach/` and the claim gates untouched; `core/main-core.tex` not
edited. Report: `2026-11-05-rees-referee-19-companion.md` (Error 0, Gap 0,
Imprecision I1--I5, Style S1--S6). Backups of every edited file before the
pass: scratchpad `bak_r19/`.

Files edited: `docs/papers/rees-hsp/main.tex`, `appendix-sde-side.tex`,
`appendix-provenance.tex`, `appendix-torsion-blackbox.tex`,
`appendix-schedule2.tex`, `appendix-free-coordinate.tex`,
`appendix-schedule3.tex`; `2026-11-05-rees-companion-restructure.md`
(addendum). No proof changed; no statement changed status.

## Findings, verified and applied

- **I1** (verified: the core's `thm:is-import` says "polynomial in $M$ and
  $\log p$, where the polynomial depends on $d$"; the companion said
  $\poly(M,\log p)$). Applied the core wording.
- **I2** (verified: P7 said "argued" while both headers and the paragraph
  after Theorem 1.2 say the tape layout is sketched). P7 now reads "the operation counts derived; the
  Turing-machine bounds ... derived in Remark `rem:sde-side-tape` as a sketch, with the absolute constants $C_1$,
  $C_2$, $C_3$ not computed" (all three constants are defined in
  `rem:is-runtime`). Headers of `rem:is-runtime` and `rem:sde-side-tape`
  gained "; Turing-machine bounds sketched, constants not computed". Header of
  `rem:two-level-threshold-size` now "Size of the two-level threshold; the
  central-moment threshold argued; AI-checked, pending human review" (its body
  already said "status: argued").
- **I3** (verified: the rotation-counting convention survived only in
  `prop:tb-count-gates`(b)). Added to `thm:bb-envelope`(iii), after the order
  finding and factoring gate count, the referee's parenthesis (rotations of
  `lem:qft-mod` as single gates; over a fixed finite gate set every count
  multiplied by $\operatorname{polylog}(\ell/\eps)$, absorbed by the $o(1)$).
- **I4** (verified). (iii) now says "In the input size
  $N = s\ell + w + \log(1/\eps)$"; the paragraph after the theorem says "For
  fixed $c$ and this $N$".
- **I5** (verified: two definitions, "cited report" and "cited note or
  report"). Both now: "a statement whose proof is given only in a source
  listed in Appendix `app:provenance`".

- **S1** Status paragraph: the clause "the corresponding claim gates of the
  reduction record (speedup allowed, total gate bound) are false" deleted; the
  sentence ends "no general SDE solver and no human review." The preceding
  plain-language list (no speedup, no novelty beyond Section 1, no implemented
  coherent receiver, no general SDE solver, no human review) is kept, and P1
  still records the gates.
- **S2** `thm:main` header "Proposed explicit-Lie theorem" -> "Main theorem"
  (as in the core). Restructure record: addendum noting that I239 synchronised
  the referee-18 core statements (`def:input-contract`, `thm:main`,
  `rem:main-solver`, `rem:is-import`, `thm:uniform-compilation`,
  `lem:collision`, `prop:classical-query`, `rem:query-separation`; the referee
  counts 9), and that its two owner items on the README and the E_2 ranges are
  done.
- **S3** $Q \to Q_{\mathrm q}$ in `thm:main`(3)--(4), the sentence after it,
  `rem:main-solver`, "The running time is polynomial in $Q_{\mathrm q}$ ...",
  and the notation-table row. `prop:coherent-receiver` keeps its own
  $Q = cSP$, now glossed "(the count $Q_{\mathrm q}$ of Theorem `thm:main`)";
  the other $Q$'s (classical query algorithm, Table of class-nine counts,
  appendices) have their own meanings and are unchanged.
- **S4** "computed from recorded artifacts" -> "computed from the recorded
  runs" (the provenance pointer was already there).
- **S5** (trivial, applied): `\mathsf{RtF}` -> `\operatorname{RtF}` (11),
  `\mathsf{Solve}` -> `\operatorname{Solve}` (10) in Appendix F;
  `^{\mathsf T}` -> `^{\mathrm T}` (4 in `appendix-free-coordinate.tex`, 2 in
  `appendix-schedule3.tex`; the referee listed 3 lines); the four `\ni`
  rewritten as `\in` (`b^\ast \in S_0^{\nu^\ast} \subseteq S_{00}`; "a set $K$
  with $0 \in K$", plus a fifth `$K \ni 0$` in the same paragraph; "$P$ is an
  ideal of $S$ and $x \in S$"; `p^{e-a_t}r_t \in \langle R_t\rangle = ...`).
  No `\mathsf` or `\ni` remains in `main.tex` or any appendix.
- **S6** Lean section: the module list after "No clean-copy build has been
  run for the remaining modules:" is now an `itemize` with six items, words,
  guard counts and status labels unchanged (`before=\raggedright` to avoid an
  overfull line from the long `\texttt` names).

## E_2(8)/E_2(9) ranges

Checked `appendix-schedule2.tex` `app:s2-scope` and the `main.tex` summary
after `prop:decoupled-sde`: both already say decided to $16993$
($\kappa = 8$) and $16633$ ($\kappa = 9$), $14281 \in E_2(8)$,
$20107 \in E_2(9)$ as the largest proved member, $1373$ listed sweep
exceptions of which $1370$ are open, $(16993, 20000]$ partly decided, and
$0.34\,\kappa^{(\kappa+1)/2}$ for $\kappa = 9$ ($20107/9^5 = 0.3405$). They
were refreshed in I239; the referee's "not refreshed" relied on the older
restructure record. The only remaining $13873$/$16363$/$18199$ are in
`prov:s2-exceptional`, where they describe what the first source report says
("there, extended by the snapshot below") and are correct; unchanged. Core:
no E_2(8)/E_2(9) numbers. No change.

## Checks

Status words in `main.tex` + appendices, before -> after: "AI-checked,
pending human review" 242 -> 242; "argued" 34 -> 34 (one added in the
`rem:two-level-threshold-size` header, one removed from P7); "conditional"
131 -> 131; "finite computation" 140 -> 140; "machine-checked" 28 -> 28;
NEEDS HUMAN VERIFICATION 24 -> 24. No new `\mathsf`, `\mathrel`,
`\begingroup`, `\aa`, `\ni`.

## Build and tests

Companion (scratchpad `build_final`, `latexmk -g -pdf`, `nice -n 19`):
exit 0, 201 pages, 0 Overfull, no undefined references or citations, no
multiply defined labels, no "Float too large". Core (scratchpad
`build_final_core`, sources unchanged): exit 0, 27 pages, same checks clean.
`pytest -q tests/tools/test_rees_paper_numbers.py`: 2 passed (a first try with
`before=\sloppy` failed the undefined-macro test, since `\sloppy` is not in
its known-command list; replaced by `\raggedright`). PDFs copied over
`docs/papers/rees-hsp/pdf/rees-companion-2026-11-05.pdf` and
`docs/papers/rees-hsp/pdf/rees-core-2026-11-05.pdf`.

## Left for the owner

- Referee 14 S2 (unlabelled headers) and S8 (letter reuse in Appendices B,
  C) remain unapplied.
- Nothing committed.
