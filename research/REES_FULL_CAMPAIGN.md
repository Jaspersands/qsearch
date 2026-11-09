# Rees "full" campaign, 2026-11-02

Goal (owner): close every remaining gap in the Rees HSP paper
(`docs/papers/rees-hsp/main.tex`), in parallel. A session's job is to make its item
complete, not just to audit it: prove what can be proved, build what can be built, and
report what still cannot be done with the smallest obstruction.

Taken as checked by AI sessions (do not redo; cite them): core steps 1–5
(`audits/reviews/2026-11-01-rees-core-proof-check.md`), priority
(`2026-11-01-rees-priority-check.md`), Cor fpt-r and ring-to-field
(`2026-11-02-rees-fpt-torsion-check.md`), the black-box pullback
(`2026-11-02-rees-black-box-check.md`), the combined schedule
(`2026-11-02-rees-combined-schedule.md`) and small-prime arity
(`2026-11-02-rees-small-prime-arity.md`). All are in `research/audits/reviews/`.

## Items (one session each)

| # | Item | Output report (`research/audits/reviews/`) | May also write |
|---|---|---|---|
| 1 | A1 priority: is the graded cover for arbitrary H known? Read papers citing arXiv:1503.09016 and arXiv:2304.08376 in full | `2026-11-02-rees-a1-priority.md` | — |
| 2 | Two-level SDE threshold near the observed ~1.5κ^{(κ+1)/2} | `2026-11-02-rees-weil-threshold.md` | `2026-11-02-rees-weil-threshold/` |
| 3 | Mechanical: the queued `dfs2` runs for κ = 7, 8, 9 | `2026-11-02-rees-dfs2-runs.md` | `.../2026-11-02-rees-schedules/small-prime/dfs2_k*.out`, built `dfs2` binary |
| 4 | Hidden codimension: restore or refute the 2^{O(k log k)} bound (`rem:codim`, `BOUNDED_CODIMENSION_HSP_REDUCTION.md`) | `2026-11-02-rees-codimension.md` | `2026-11-02-rees-codimension/` |
| 5 | Flat subspace source (`sec:subspace`, `thm:subspace-source`, `REES_SUBSPACE_SYMMETRY_SOURCE.md`) | `2026-11-02-rees-subspace-source.md` | `2026-11-02-rees-subspace-source/` |
| 6 | Prime-power word compiler for class c ≥ 5 (closes the black-box e > 1 gap; `UNIVERSAL_LAZARD_WORD_COMPILER.md`, `CLASS_FOUR_PRIME_POWER_INPUT.md`) | `2026-11-02-rees-prime-power-compiler.md` | `2026-11-02-rees-prime-power-compiler/` |
| 7 | Gate compilation and classical filters (`sec:uniform-compilation`, `thm:uniform-compilation`, `sec:classical-landscape`, `prop:conjugation`) | `2026-11-02-rees-compilation-filters.md` | `2026-11-02-rees-compilation-filters/` |
| 8 | Lean: rebuild in a copy, confirm the 180 guards of `tab:lean-modules`, and extend the kernel-checked boundary toward general class | `2026-11-02-rees-lean.md` | `2026-11-02-rees-lean/` (new `.lean` files; never edit `formal/`) |
| 9 | Implementation: deterministic Ivanyos–Santha Section 3 SDE solver (Schedule 1) for small fixed degree, with exact tests | `2026-11-02-rees-is-solver.md` | `theorems/rees_is_sde_solver.py`, `tests/test_rees_is_sde_solver.py` |
| 10 | Implementation: exact end-to-end state-vector simulation of the whole algorithm on small groups, recovering H | `2026-11-02-rees-end-to-end.md` | `theorems/rees_end_to_end_sim.py`, `tests/test_rees_end_to_end_sim.py` |
| 11 | Candidate full manuscript: apply every ranked text fix from the six reports above to a COPY | `2026-11-02-rees-manuscript-draft.md` (change log) | `docs/papers/rees-hsp/main-full-draft.tex` |
| 12 | Native application: a motivated problem that reduces to the Rees setting and is not classically easy (`2026-10-30-rees-application-selection.md`) | `2026-11-02-rees-application.md` | `2026-11-02-rees-application/` |

## Rules for every session

- Start with `research/STATE.md` and `research/TRAPS.md`. Read `main.tex` and notes only at the
  anchors you need (grep first). Never read `research/AGENT_HANDOFF.md` or
  `research/RESEARCH_PRIORITY_DECISION.md` whole. Tools: `research/TOOLBOX.md`; Python
  `/opt/anaconda3/bin/python`; Lean `lake` at `~/.elan/bin/lake`, in a copy only.
- Twelve sessions share this checkout, which has many uncommitted changes. Write ONLY the files in
  your row. Do not edit `main.tex`, notes, registries, claim gates, `STATE.md`, `AGENT_HANDOFF.md`,
  `MECHANICAL_FOLLOW_UP_PLAN.md`, `formal/` or `docs/outreach/`. The parent session folds results in.
  Commit nothing, switch no branch, contact no one.
- Run tests only for your own files:
  `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python -B -m pytest -q -p no:cacheprovider <your test>`.
  Compare `git status --short` before and after.
- Run long jobs in the background with a time limit, and do not end your turn while your own
  jobs are still running. Save every script output next to the script.
- Literature: fetch full texts and cite theorem numbers; abstracts and snippets support no verdict.
  Use standard WebSearch first, and extended only if results are thin.
- Label every claim proved / exact computation / Lean / float check / argued. A failed claim is a
  result: give the smallest instance, and do not patch around it.
- End the report with: the exact statement that now holds (quantifiers, access model, charged
  costs); what is still missing; the claim gates that must stay false; text fixes for `main.tex`
  (listed, not applied, except in item 11's copy).
