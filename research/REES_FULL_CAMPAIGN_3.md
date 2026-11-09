# Rees "full" campaign, round 3 (2026-11-02 night)

Owner instruction: work all night to make the Rees paper full, and write everything down
for Codex before usage runs out. The ranked gaps are in `REES_FULL_CONTINUATION.md`. Rules
are as in `REES_FULL_CAMPAIGN_2.md` ("Shared rules"). The integrator session
(`rees-r2-01-integrator`) remains the only writer of `main.tex` and the five appendix files.
Each other session writes only its own new files.

| # | Item | Output (`research/audits/reviews/` unless stated) | May also write |
|---|---|---|---|
| 1 | Appendix proof of `thm:free-coordinate` (K7) | `2026-11-02-rees-free-coordinate-appendix.md` | `docs/papers/rees-hsp/appendix-free-coordinate.tex`, same-named folder |
| 2 | Integrator pass 4: referee M4 (define the two-level contraction, T_S, E_2, fair-bit sampling, m_+, q_+ in the body) and the referee minors that need no owner decision | integration log rows I79 onward | paper folder |
| 3 | Schedule 2 square gap: prove a two-level threshold near the observed 1.5κ^{(κ+1)/2}, or find an obstruction | `2026-11-03-rees-threshold-3.md` | same-named folder |
| 4 | Scalable gate-level circuit generator for general (L, c, p), tested at c = 3 | `2026-11-03-rees-circuit-2.md` | `theorems/rees_circuit_general.py`, `tests/test_rees_circuit_general.py` |
| 5 | dfs2 κ = 8 LIMIT reruns (local session) plus a full κ = 8, 9 scan to 20000 at 5·10⁷–5·10⁹ nodes in a CLOUD session (`rees-cloud-dfs2`, no commit or push; its results are only in that session's final message, so read them with list_events and copy them into the dfs2-complete report). Local reruns, at 5·10⁷ nodes, κ = 9 chunks (session `rees-r2-04-dfs2`) | `2026-11-02-rees-dfs2-complete.md` | `2026-11-02-rees-schedules/small-prime/` |

Items 3 and 4 run as background subagents of the parent session, since sessions can't be started from automated turns. Items 1, 2 and 5 are sessions. When an item lands, the parent session checks it and forwards its "Proposed paper text" to
the integrator. If usage runs out first, Codex continues from `REES_FULL_CONTINUATION.md`, and
the state of each item is whatever its output file says.
