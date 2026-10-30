# Agent Delegation

You have my standing permission to create and use subagents without asking me
whenever parallel work or independent review would materially improve this
project. Choose a sensible number, keep tasks focused, and report their
conclusions. This permission does not authorize extra Git, network, or
external-service actions.

# Research Pass Protocol (Codex research passes)

`research/GOAL.md` is the binding owner policy. At the start of a pass, read
`research/STATE.md` (current state) and `research/TRAPS.md` (traps and usage
rules). Together they replace rereading `research/AGENT_HANDOFF.md` and
`research/RESEARCH_PRIORITY_DECISION.md`: search those for a specific term
and never read them whole. If `STATE.md` is older than the newest Codex
research entry in the handoff, refresh it from that entry first.
`research/TOOLBOX.md` lists the computer algebra tools (Sage, GAP, PARI,
Singular, fpylll, cvc5, pdftotext) and how to call them.

At the end of a pass:

- Rewrite `research/STATE.md`, covering the "Now" section and any rows that
  changed. Priority changes go there; `RESEARCH_PRIORITY_DECISION.md` needs
  no new entries.
- Add one entry at the top of `research/AGENT_HANDOFF.md`: a
  `## YYYY-MM-DD Title` heading (the cockpit reads these) and about 15
  lines. Cover the claim proved, refuted or left conditional; its
  assumptions and access model; the strongest classical baseline; the claim
  gates that must stay false; the next hard question; and a pointer to the
  topic note that holds the exact statements.
- Add Gemini's mechanical items at the top of
  `research/MECHANICAL_FOLLOW_UP_PLAN.md`, and point to them from the
  handoff entry.

Brief helper agents with the files they need, `research/STATE.md` and the
interpreter `/opt/anaconda3/bin/python`. Don't point them at the archives.
