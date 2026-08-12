# Research Goal

Maximize this repository's expected contribution to discovering or falsifying
a genuinely groundbreaking quantum algorithm comparable in significance to
Shor's algorithm.

## Binding Model-Allocation Policy

Use high-capability Codex time for work whose outcome materially depends on
deep mathematical judgment:

- theorem derivation and proof repair;
- counterexample and no-go construction;
- asymptotic and representation-theoretic analysis;
- mechanism selection and research-direction triage;
- decisive falsifier and experiment design;
- identifying reductions, query-model gaps, and classical simulations.

Defer low-judgment implementation to Gemini 3.6 Flash through Antigravity:

- repetitive registry, CLI, runner, README, and UI wiring;
- artifact refreshes and schema-preserving migrations;
- formatting, copied dispatch code, and broad routine validation;
- mechanical test expansion after the mathematical contract is fixed.

Before Codex usage is exhausted, record exact theorem statements, assumptions,
claim gates, counterexamples, unresolved obligations, acceptance tests, and the
next hard derivations in `research/AGENT_HANDOFF.md`. Record executable
mechanical follow-up in `research/MECHANICAL_FOLLOW_UP_PLAN.md`. Gemini must
preserve those mathematical boundaries and must not promote finite evidence or
passing tests into an algorithmic speedup claim.

Running out of one model's usage is a handoff event, not completion of this
research goal.

This allocation is mandatory during autonomous runs: repeatedly choose the
highest-value unresolved theorem, counterexample, asymptotic boundary, or
research-direction decision for Codex. Do not consume the remaining
high-capability budget merely to keep the pipeline busy. Leave a continuously
updated, executable queue of lower-judgment work for Gemini 3.6 Flash so that
Antigravity can continue immediately when Codex usage ends.

The allocation invariant is **reasoning first, mechanics later**. While Codex
is available, it must spend substantially more effort on hard derivations,
counterexamples, asymptotic analysis, and research triage than on small or
routine implementation tasks. Routine work should be documented precisely
enough that Gemini 3.6 Flash can execute it in Antigravity without rediscovering
the mathematical intent. At Codex exhaustion, Gemini continues the mechanical
queue; it does not reinterpret open conjectures, weaken falsifiers, or promote
experimental evidence into theorem or speedup claims.

## Nonnegotiable Research Discipline

- Do not restore legacy tiny-circuit search or generate toy oracle problems.
- Treat every apparent quantum advantage as suspect until it survives the best
  legal classical baselines under the same access model.
- Prefer structural mechanisms, reductions, falsifiers, and proof obligations
  over demos or incremental benchmarks.
- Distinguish finite evidence, asymptotic theorems, implementable measurements,
  decoders, end-to-end algorithms, and complexity separations at every stage.
