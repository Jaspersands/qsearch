# Rees "full" campaign, round 2 (2026-11-02)

Owner instruction: run many parallel sessions on the priorities for a complete Rees paper,
and incorporate the results into the paper whenever they are ready. No further owner
permission is needed for paper edits. Round 1 is `REES_FULL_CAMPAIGN.md`, with its reports
in `research/audits/reviews/2026-11-02-rees-*.md`. Its candidate manuscript is
`docs/papers/rees-hsp/main-full-draft.tex`, with the change log in
`2026-11-02-rees-manuscript-draft.md`. Treat those as given; do not redo them.

## Paper ownership (read this first)

- **Only the integrator session (item 1) edits** `docs/papers/rees-hsp/main.tex`,
  `references.bib`, `numbers.tex`, `make_numbers.py` and `README.md` in that folder.
- **Appendix writers (items 14–18)** each own one new file
  `docs/papers/rees-hsp/appendix-<name>.tex`. Use only macros that `main.tex` already defines,
  and start the file with a `\section{...}` and a `\label{app:<name>}`. Test-compile it
  by copying `main.tex` into your scratchpad, adding `\appendix\input{...}` before
  `\bibliography`, and building there. The integrator `\input`s your file.
- **Every other session** puts paper text in a section of its own report titled
  "Proposed paper text". Give exact LaTeX, the target location (section label or
  line), and the status label. The integrator folds it in.
- Status labels never rise above what the evidence supports. "AI-checked, pending human
  review" stays on every claim. No session flips a claim gate in any JSON.

## Items

| # | Item | Model | Output (`research/audits/reviews/` unless stated) | May also write |
|---|---|---|---|---|
| 1 | Integrator: make `main.tex` the full paper | Opus high | `2026-11-02-rees-integration-log.md` | paper folder files above; `docs/papers/rees-hsp/archive/` |
| 2 | Referee: an unanchored adversarial review of the whole draft | Opus high | `2026-11-02-rees-referee.md` | — |
| 3 | Two-level threshold, round 2: close the square gap | Opus high | `2026-11-02-rees-threshold-2.md` | `2026-11-02-rees-threshold-2/` |
| 4 | Finish the dfs2 scans for κ = 8, 9 up to 20000 | Sonnet low | `2026-11-02-rees-dfs2-complete.md` | `2026-11-02-rees-schedules/small-prime/dfs2_k{8,9}_*.out` |
| 5 | An efficient SDE solver at arity o(a²), or linear arity at small p | Opus high | `2026-11-02-rees-linear-arity.md` | `2026-11-02-rees-linear-arity/` |
| 6 | Schedule 3 without 2^128 rejection trials | Opus high | `2026-11-02-rees-schedule3-cost.md` | `2026-11-02-rees-schedule3-cost/` |
| 7 | Black-box total cost envelope for the free-pullback route (gap C6), plus the all-prime composition with Imran–Ivanyos | Opus high | `2026-11-02-rees-bb-envelope.md` | `2026-11-02-rees-bb-envelope/` |
| 8 | Audit every note the paper cites as "not re-audited" or "not reproduced" (e.g. `REES_MIXED_SPECTRAL_SOURCE.md`, `REES_FULL_GRADE_PARAMETER_BOUND.md`) | Opus high | `2026-11-02-rees-cited-notes.md` | `2026-11-02-rees-cited-notes/` |
| 9 | Classical lower bound: query complexity of HSP in this family, so the paper can state the separation | Opus high | `2026-11-02-rees-classical-lower-bound.md` | `2026-11-02-rees-classical-lower-bound/` |
| 10 | Lean: promote the four round-1 general-class files into `formal/` with Audit guards, then extend (class-four BCH group law, general-law hypotheses) | Opus high | `2026-11-02-rees-lean-2.md` | `formal/` (this session only) |
| 11 | Gate-level circuit for the smallest instance (Heis(F₃) cover), simulated with Qiskit 2.3 | Opus high | `2026-11-02-rees-circuit.md` | `theorems/rees_circuit.py`, `tests/test_rees_circuit.py` |
| 12 | Scale the end-to-end simulator: real IS solver, class 4, combined rule | Opus medium | `2026-11-02-rees-e2e-scale.md` | `theorems/rees_end_to_end_ext.py`, `tests/test_rees_end_to_end_ext.py` |
| 13 | A1 priority, remaining gap: the 4 missing Imran–Ivanyos citers, plus a Scholar sweep of Ivanyos–Santha citers | Sonnet medium | `2026-11-02-rees-a1-citers.md` | — |
| 14 | Appendix: Schedule 2 full proof (symmetric and decoupled contraction, thresholds T_W and T_A) | Opus high | — | `docs/papers/rees-hsp/appendix-schedule2.tex` |
| 15 | Appendix: Schedule 3 full proof, including uniformity in c | Opus high | — | `docs/papers/rees-hsp/appendix-schedule3.tex` |
| 16 | Appendix: subspace source full proof, including the determinant-character step | Opus high | — | `docs/papers/rees-hsp/appendix-subspace.tex` |
| 17 | Appendix: ring-to-field and black-box full proofs (stop rules, ker Φ, Sylow split) | Opus high | — | `docs/papers/rees-hsp/appendix-torsion-blackbox.tex` |
| 18 | Appendix: hidden-codimension reduction full proof | Opus high | — | `docs/papers/rees-hsp/appendix-codimension.tex` |

Sources for the appendices are the round-1 reports: `2026-11-01-rees-core-proof-check.md`
§§5.4–5.5, `-small-prime-arity.md`, `-weil-threshold.md`, `-fpt-torsion-check.md`,
`-black-box-check.md`, `-subspace-source.md` and `-codimension.md`, plus the notes they
cite. An appendix proof must be complete and self-contained at journal level. Do not copy a
report's prose; write the proof.

## Shared rules

- Start with `research/STATE.md` and `research/TRAPS.md`. Read `main.tex` (or the draft),
  the notes and the reports only at the anchors you need; grep first. Never read
  `research/AGENT_HANDOFF.md` or `research/RESEARCH_PRIORITY_DECISION.md` whole. Tools are in
  `research/TOOLBOX.md`. Python is `/opt/anaconda3/bin/python`. Lean is `~/.elan/bin/lake`.
- About 18 sessions share this checkout, which has many uncommitted changes. Write ONLY the
  files in your row. Do not edit `STATE.md`, `AGENT_HANDOFF.md`, `MECHANICAL_FOLLOW_UP_PLAN.md`,
  registries, claim gates or `docs/outreach/`. Commit nothing, switch no branch, contact no one.
- Run tests only for your own files:
  `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python -B -m pytest -q -p no:cacheprovider <your test>`.
  Compare `git status --short` before and after.
- Save every script output inside your own folder; nothing goes in the app notes folder.
  Run long jobs in the background with a time limit, and do not end a turn while your own
  jobs are still running.
- Literature: fetch full texts and cite theorem numbers. Use standard WebSearch first, and
  extended only if results are thin.
- Label every claim: proved / exact computation / Lean / float check / argued. A failed
  claim is a result. Give the smallest instance, and do not patch around it.
- End every report with: the exact statement that now holds; what is still missing; the
  claim gates that must stay false; and "Proposed paper text" (or "none").
