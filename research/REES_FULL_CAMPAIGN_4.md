# Rees "full" campaign, round 4 (2026-11-02/03 night)

Owner instruction (2 Nov, late): work all night to make the Rees paper full, use all
remaining usage and the cloud credits on it, and write everything down for Codex. The ranked
gaps are in `REES_FULL_CONTINUATION.md`; round 3 is in `REES_FULL_CAMPAIGN_3.md`.

## Shared rules (same as round 2, restated)

- Start with `research/STATE.md` and `research/TRAPS.md`. Grep `main.tex`, the appendices and
  the reports, and read only the anchors you need. Never read `research/AGENT_HANDOFF.md` or
  `research/RESEARCH_PRIORITY_DECISION.md` whole. Tools are in `research/TOOLBOX.md`. Python is
  `/opt/anaconda3/bin/python`, and Lean is `~/.elan/bin/lake`.
- Write ONLY the files in your row. Only the integrator (`rees-r2-01-integrator`) edits
  `docs/papers/rees-hsp/main.tex` and `appendix-*.tex`. Everyone else puts paper text under
  "Proposed paper text" in their report: exact LaTeX, its target and its status label.
- Commit nothing, push nothing, switch no branch, flip no claim gate, contact no one, and
  leave `docs/outreach/` alone. Keep "AI-checked, pending human review" on every claim.
- The machine is shared and loaded. Run at most 2 CPU-heavy jobs at once, niced and
  time-limited. Don't end a turn while your own jobs are still running.
- Label every claim: proved / exact computation / Lean / float check / argued. A failure is a
  result: give the smallest instance, and don't patch around it.
- End every report with: the exact statement that now holds; what is still missing; the
  claim gates that must stay false; and "Proposed paper text" (or "none").

## Items

| # | Item | Where | Output (`research/audits/reviews/`) | May also write |
|---|---|---|---|---|
| 1 | Unanchored proof check of Appendix A (Schedule 2) | local | `2026-11-03-rees-check-app-a.md` | same-named folder |
| 2 | Unanchored proof check of Appendix B (Schedule 3) | local | `2026-11-03-rees-check-app-b.md` | same-named folder |
| 3 | Unanchored proof check of Appendix C (subspace source) | local | `2026-11-03-rees-check-app-c.md` | same-named folder |
| 4 | Unanchored proof check of Appendix D (torsion, black box) | local | `2026-11-03-rees-check-app-d.md` | same-named folder |
| 5 | Unanchored proof check of Appendix E (codimension) | local | `2026-11-03-rees-check-app-e.md` | same-named folder |
| 6 | Unanchored proof check of the body's core proof: §§2–4 and the assembly of Theorem `thm:main` | local | `2026-11-03-rees-check-core.md` | same-named folder |
| 7 | A self-contained core paper per referee F1, as a SEPARATE file: §2, the cover and descent, Schedule 1, compilation, the proof of Thm main, plus an outlook without theorem environments. Do not replace `main.tex`. | local | `2026-11-03-rees-core-paper.md` | `docs/papers/rees-hsp/core/main-core.tex` (and a copy of the bib and numbers there if needed) |
| 8 | Lean: formalize the triangular two-level SDE solver (`prop:triangular-sde`) and the Chevalley–Warning witness-existence bound κa+1 over `ZMod p` | local | `2026-11-03-rees-lean-3.md` | new `formal/Formal/ReesSde*.lean` and their Audit.lean guards (this session only) |
| 9 | End-to-end exact simulation of the mixed-source substitution (`rem:mixed-source`) into the Rees core, small instances | local | `2026-11-03-rees-mixed-source-sim.md` | `theorems/rees_mixed_source_sim.py`, `tests/test_rees_mixed_source_sim.py` |
| 10 | Cloud: an o(a²)-column SDE solver, or hardness at fixed κ | cloud | final message (copy it into `2026-11-03-rees-cloud-linear-arity.md`) | — |
| 11 | Cloud: E_2(9) on [20001, 100000]. The observed size 1.5κ^{(κ+1)/2} ≈ 88,600 at κ = 9, so the scan to 20000 by `rees-cloud-dfs2` cannot complete E_2(9). κ ≥ 10 would need scans past 4·10⁵ and is not run | cloud | final message (copy it into `2026-11-03-rees-cloud-dfs2-k9-high.md`) | — |
| 12 | Cloud: A1 citers through Google Scholar and the publisher pages, from a cloud IP | cloud | final message (copy it into `2026-11-03-rees-cloud-a1.md`) | — |

| 13 | A second unanchored referee pass over the 106-page main.tex, run as a subagent of the parent and written incrementally | local | `2026-11-03-rees-referee-2.md` | same-named folder |

Cloud sessions see only the pushed `main`, which lacks this work, and must not push (the repo
is public). Their briefs carry every input they need, and the parent copies their final
messages into the files above. If usage runs out, Codex continues from
`REES_FULL_CONTINUATION.md`, and each row's output file is that item's state.
