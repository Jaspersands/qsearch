# Traps

These rules distill about 1,250 "do not" sentences in the handoff, priority
and mechanical-plan archives, plus the registry audits (October 2026).
Read this page instead of those archives. Add traps after they cost a pass;
delete closed ones and keep this under120 lines. Paths are relative to
`research/`; commands run from the repo root.

## Choosing what to work on
1. Choose the next pass by its value outside this repo, not by the gap the
   last pass left, unless that gap is the decisive obstacle to an
   externally valuable result. Don't add another variant, sweep, fixture or
   wrapper just to keep work moving.
2. Before starting a line of work, check prior work:
   `/opt/anaconda3/bin/python tools/corpus/cli.py been-tried "<idea>"` for
   this repo, then a literature search. 73% of the negative registry
   restates or sits next to published work.
3. Work on a task that has motivation outside this repo. Don't build an
   application out of an unresolved residual.

## Before building anything quantum
4. First run the track's standard classical attacks on the exact instance.
   A classical competitor is the top failure mode: it killed 32% of
   registry records. `tools/corpus/cli.py baselines "<idea>"` names the
   catalogued attacks. Run them with the real algebra tools in
   `TOOLBOX.md` (Sage, PARI, GAP, Singular, fpylll), not hand-rolled code.
5. Charge every oracle and supplied input. Never plant secrets, read the
   truth, use free inverses, or supply hidden advice such as a target
   End/Hom lattice.
6. Keep source-law and coherence bookkeeping explicit. A frozen bank is not
   fresh IID data. Never silently discard workspace, renormalize or
   postselect.

## Claims
- Trace signs: P_i(T)=det(1-TF) has linear coefficient -Tr(F). For smooth
  surfaces with H1=H3=0, #X=1+q²-[T]P2; do not reuse the curve sign.
7. Finite scans and fixtures can only falsify. Never use them as evidence
   for all n.
8. An incomplete attack, an UNKNOWN, a missing backend or a mixing
   obstruction does not show hardness or a general no-go.
9. Never claim a speedup, novelty or a "Shor-like" result. Polynomial query
   complexity is not efficient time, and huge sufficient query counts are
   not lower bounds.
10. Never infer a theorem, or that one doesn't apply, from an abstract,
    slides or a paper you couldn't open. Leave the question UNKNOWN.
11. Check every reviewer's or agent's claim against the source before you
    act on it. An external AI review here cited a nonexistent axiom
    (`total_sde_policy_hyp`) and a "ten-feature gate"; see
    `manuscripts/REES_FOUR_PILLAR_CORRECTIONS.md`. Passing tests once hid
    nontermination. Reviewers also read stale notes: check the newest
    handoff entry on the topic.

## Scope guards to keep word for word

- "The corrected search contract is: specify a motivated native input and
  verifiable output; give a paid coherent reduction with fixed promises;
  choose the strongest applicable quantum upper bound; run each classical
  attack only under its actual hypotheses; and leave unmatched cases
  UNKNOWN, not hard." (REES_FOUR_PILLAR_CORRECTIONS.md section 6)
- Rees wording: "proposed fixed-class, growing-prime polynomial-time
  composition, pending independent correctness and priority review".
- "Classical retries reuse measured labels, not consumed quantum copies."
  "Never reprepare the quantum bank, rerun central measurement, or apply a
  guessed dilation during these retries. An exhausted clock means ABORT."
- "Never turn a returned single VALID candidate into a complete-list
  singleton." "Actual list size must not change the branch normalization."
- Siegel: "Do not add a target End/Hom lattice as hidden advice." "Scalar
  and even non-scalar commuting automorphisms can give zero; do not declare
  the general weak-input problem classically solved." This route uses
  known degree-two HPGP, not Rees.
- "Crucial limitation: the obstructing starts ARE SOLUTIONS. No lower bound
  on first-witness hitting from an unconditioned uniform codeword follows."
  (INVERSE_TRACE_GIBBS_TARGET.md)

## Process

12. Codex does the theory. Low-judgment wiring (registry, CLI, runner,
    README, UI), artifact refreshes and mechanical test expansion go to
    Gemini through `MECHANICAL_FOLLOW_UP_PLAN.md`. Research notes and the
    handoff stay with Codex.
13. Use `/opt/anaconda3/bin/python` for everything, and say so in every
    helper brief. `/usr/local/bin/python3` has no flint or z3.
14. Run only the tests the change affects. Never claim the full suite is
    green. Failures listed in `../tests/KNOWN_FAILURES.txt` predate you;
    leave them to Gemini. Never edit claims or repin evidence to make
    tests pass.
15. Never test against a file another actor is still writing. Codex
    doesn't commit or push; Git checkpoints are Gemini's.
16. Don't re-acknowledge closed reviews or repeat status boilerplate
    ("PROGRESS; goal ACTIVE", the registry hash, dirty-file lists).
17. Never run `docs/papers/rees-hsp/make_numbers.py`, not even with
    `--check`: it rewrites `numbers.tex` before checking. Use
    `tests/tools/test_rees_paper_numbers.py`, or import its functions
    read-only.

## Usage: spend it on thinking, not overhead
- **Batch.** One command reading several files or running several checks
  beats small calls, each of which resends the context (about120K tokens).
- **Rituals only at milestones.** Run `qsearch.py validate`, registry
  hashes, `git status`/`diff` and site checks once per milestone, not
  every pass.
- **Short output.** Use `pytest -q`, and `head`/`tail` on long output.
  Never print a large file whole.
- **Helpers.** Default to at most three per round. Use more only when the
  work really splits into more independent pieces. Brief each one with the
  files it needs and `research/STATE.md`, never the handoff. Helpers get no
  Git, network or external-service actions (`AGENTS.md`): fetch papers
  yourself and hand them over as local files.
- **Claude API.** Owner-authorized paid research reviews use
  `CLAUDE_RESEARCH_WORKFLOW.md`: explicit context, saved usage, verified findings;
  no automatic claim promotion or unknown-cost retry.
- **Effort matched to the job.** Use the highest effort for core reasoning
  and adversarial maths. Use lighter settings (e.g. `gpt-6.1-sol` at `high`)
  for source reads, tests or bookkeeping.
- **Review matched to the claim.** Get an independent review for anything
  that would move a row of `STATE.md` between Live, Parked and Closed.
  Skip it for small edits. Prior-art checks change decisions most often;
  plain confirmation reviews confirmed 58% of the time.
