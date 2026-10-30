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
research entry in the handoff, refresh it from that entry first: compare
the title in `STATE.md` with `grep -m1 '^## 20' research/AGENT_HANDOFF.md`
(several entries can share a date).
`research/TOOLBOX.md` lists the computer algebra tools (Sage, GAP, PARI,
Singular, fpylll, cvc5, pdftotext) and how to call them.

After each hard derivation, as `GOAL.md` requires, and at the end of every
pass:

- Add an entry at the top of `research/AGENT_HANDOFF.md` with a
  `## YYYY-MM-DD Title` heading (the cockpit reads these). State exactly the
  claim proved, refuted or left conditional; its assumptions, quantifiers
  and access model; the strongest counterexample or classical baseline; the
  claim gates that must stay false; the next hard question; and the next
  command, expected artifact and acceptance test. Keep it as short as that
  allows. Long derivations go in the topic note, and the entry points to
  it.
- Add Gemini's mechanical items at the top of
  `research/MECHANICAL_FOLLOW_UP_PLAN.md`, and point to them from the
  handoff entry.
- At the end of the pass, rewrite `research/STATE.md`, covering the "Now"
  section and any rows that changed. Priority changes go there;
  `RESEARCH_PRIORITY_DECISION.md` needs no new entries.

Brief helper agents with the files they need, `research/STATE.md` and the
interpreter `/opt/anaconda3/bin/python`. Don't point them at the archives.
