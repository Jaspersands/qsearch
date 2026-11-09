# Rees "full" paper: continuation brief for Codex (2026-11-02)

The owner wants the Rees HSP paper made "FULL": a complete, self-contained, journal-level
paper whose every step is proved or explicitly conditional. Two rounds of parallel Claude
sessions ran on 2 November (`REES_FULL_CAMPAIGN.md`, `REES_FULL_CAMPAIGN_2.md`). This page
says where things stand and what is left, ranked. Read `STATE.md` and `TRAPS.md` first.

## Standing rules (owner)

- The paper may be edited locally at any time, with no permission needed. Archive the old
  `main.tex` in `docs/papers/rees-hsp/archive/` before any big replacement. Build check:
  `latexmk -pdf` in a scratchpad copy (main.tex, numbers.tex, references.bib,
  appendix-*.tex), then `make_numbers.py --check` and `tests/tools/test_rees_paper_numbers.py`.
- Commit nothing and push nothing without the owner's OK. The repo is PUBLIC.
  `docs/outreach/` is unsent; do not touch it.
- Never flip a claim gate in `research/reductions/rees_hsp_reduction.json`. Keep "AI-checked,
  pending human review" on every claim.

## Where things are

- **Paper:** `docs/papers/rees-hsp/main.tex`, 133 pages after the parent's 11-04 passes (I137–I161) (clean build:
  no overfull box, no LaTeX or hyperref warning), with appendices A–F
  (`appendix-{schedule2,schedule3,free-coordinate,subspace,torsion-blackbox,codimension}.tex`,
  in that order, now owned by the integrator). Change log, with rows I1–I189 and judgement calls K1–K31:
  `audits/reviews/2026-11-02-rees-integration-log.md`. Pass 3 folded in Lean-2, the circuit and
  the scaled simulator (I66–I74) and fixed K13–K15 (I75–I77). I78 is the parent's
  `\leavevmode` anchor fix. Pass 4 did referee M4 and minors m3, m9 and m11 (I79–I86). Pass 5
  folded in the free-coordinate appendix (I87–I94). Pass 6 folded in the round-4 checks of the
  core, Appendix A and the codimension appendix (now F) (I95–I105). Pass 7 folded in the
  Appendix B check (I106–I112; I112 is the label-law qualifier) and the threshold-3 obstruction
  with its verified BGP citation (I113–I114). Pass 8 folded in the round-4 checks of
  Appendices D and E (reviewers' C and D: I115–I122, error fixes 9a, P7 and F1 first), Lean-3
  (I123, guards recounted: total 396) and the mixed-source simulation (I124). All six
  round-4 checks are now folded in. Pass 9 folded in the second referee read
  (`2026-11-03-rees-referee-2.md`): thm:main restated as Schedule 1 with the Ivanyos–Santha
  import isolated as `thm:is-import`, `lem:s3-hybrid` on the canonical domain, prop:triangular-sde
  "deterministic given g", and the thm:bb-envelope counts pointed to or labelled argued
  (I125–I131). Its labelling and form items are open for the owner (K29). Pass 10 folded the
  general circuit generator into "Gate-level control" (I132). Pass 11 added the block-splitting
  proof as Appendix C, Section `app:fc-split`, and corrected the body sentence (I133–I134). Pass 12 added the threshold-4 negative result to
  `rem:two-level-threshold-size` (I135). Pass 13 folded the sparse class-four circuit simulation
  into "Gate-level control" (I136; K30 is a float-rounding clause for the owner). The last row is I136. dfs2 κ = 8, 9 (#4) is not folded in. Pre-campaign copy:
  `docs/papers/rees-hsp/archive/main-2026-11-02-before-full.tex`.
- **Reports:** `audits/reviews/2026-11-0{1,2}-rees-*.md`, with scripts in the same-named
  folders. Each ends with "exact statement that now holds / still missing / gates /
  proposed paper text".
- **Code:**
  - `theorems/rees_is_sde_solver.py`: Schedule 1 solver.
  - `theorems/rees_end_to_end_sim.py` and `theorems/rees_end_to_end_ext.py`: exact simulators.
    The second uses the real solvers at Rule W arity and runs class four on n5(F_11).
  - `theorems/rees_circuit.py`: a Qiskit gate-level circuit for Heis(F_3), all 19 subgroups.
  - `theorems/universal_lazard_words.py`: now has `modulus=p^e`.
  - Tests for each are in `tests/`.
- **Lean:** eight general-class and class-four modules were promoted into `formal/Formal/`
  (Audit.lean: 403 guards, all standard axioms). The clean-copy
  `lake --no-cache build --wfail` succeeded (3507 jobs; log in
  `audits/reviews/2026-11-02-rees-lean-2/build_clean.log`). For c = 3, 4 the group law and
  the measured receiver are unconditional; for c ≥ 5 they are conditional on the Lazard law.

## Rounds 3 and 4 in flight (11-02 night)

Round 4 (`REES_FULL_CAMPAIGN_4.md`) adds:
- unanchored proof checks of appendices A–E and of the core (items 1–6);
- a separate core paper at `docs/papers/rees-hsp/core/main-core.tex` (item 7);
- Lean for the SDE witness bound and the triangular solver (item 8);
- a mixed-source simulation (item 9);
- three cloud jobs (items 10–12) that report only in their final messages: read them with `list_events` and copy them into the output files named there.

A proof-check verdict of "gap" or "error" outranks everything below: fix the paper first.

### Round 3

See `REES_FULL_CAMPAIGN_3.md`. Each item's output file is its state. If a file is missing, that item did not finish and should be rerun from the brief in that table.

## Paper status at 11-02 ~23:00 (parent-verified)

`main.tex`: 106 pages, after integrator pass 8, with log rows through I124. The parent
rebuilt it in a scratchpad. Build exit 0, with no dest warnings, no overfull boxes and no
undefined refs or cites. Appendices A–F are \input. All six round-4 proof checks (A–E and
core) and Lean-3 are folded in. Lean: `Audit.lean` has 434 guards in total; `tab:lean-modules`
covers 396 of them. `core/main-core.tex` is 26 pp., holds only sources, and closes check-core
G1/G2. The circuit-generator subagent and the four cloud jobs had not reported at this time.

## Referee 2 (11-03, `audits/reviews/2026-11-03-rees-referee-2.md`)

Verdict: major revision, with no error in the proof of `thm:main` for any H. The integrator applied
the gaps in pass 9 as I125–I131 (build clean, 106 pp.); the form items are K29:
- P1–P2: `thm:main` as Schedule 1, plus the Ivanyos–Santha import, which must return the roots.
- P4: Appendix B's `lem:s3-hybrid` domain.
- The counts in `thm:bb-envelope` are proved nowhere. (Closed at I144: Appendix D `app:tb-counts` proves (i), (ii) as corrected, (iv) and E_W(c); the gate counts of (iii) are proved under the stated hypotheses (H1)–(H3), K31.)
- `prop:triangular-sde`'s "deterministic" needs a non-residue.

Open for the owner: status tags that record who has read a proof rather than what a statement
depends on, 101 file pointers, and the changelog in the paper. `core/main-core.tex` is the
structural answer to these.

## Circuit generator (11-03, `audits/reviews/2026-11-03-rees-circuit-2.md`)

`theorems/rees_circuit_general.py` takes any Lazard algebra with c < p. It reproduces
Heis(F_3) gate for gate, and on n4(F_5) it covers 9 subgroups, 5 of them non-normal, with exact
checks and 18/18 recoveries; the largest simulated is n4(F_7). The parent reran the fast tests:
59 passed and 14 slow skipped (`REES_SLOW=1` runs them, about 8.5 min). Gates per
multiplication are O(p^3 log p), a small-p construction. Class four is blocked by memory: a
sparse coset-support backend would fix that (built in `-circuit-3.md`, folded in at I136). The label "<e2,e3,e4> normal" at
`theorems/rees_end_to_end_sim.py:924` is wrong (the subgroup is ⟨e2,e3⟩, non-normal), but the
paper does not depend on it. Sent to the integrator.

## dfs2 update (11-03, `audits/reviews/2026-11-02-rees-dfs2-complete.md`)

κ = 8 at 5·10⁷ nodes: 4073, 4129, 4153 and 4201 are INFEASIBLE, so the largest known E_2(8)
prime is now 4201 (it was 4057). The remaining κ = 8 and κ = 9 ranges to 20000 are still running
locally, and the cloud job `rees-cloud-dfs2` covers the same ranges at larger budgets. E_2(8)
and E_2(9) are not complete, so the paper must keep saying that only κ ≤ 7 is exact.

## Last item launched (11-03)

A subagent is proving the block-splitting sentence after `prop:rc-lower`, which so far is proved only in
`-schedule3-cost.md`. Its output is `audits/reviews/2026-11-03-rees-block-splitting.md`,
written incrementally. It is COMPLETE: the claim holds, as one lemma and two propositions, with a
wording correction (the trial cap is per sub-solver, not per node). **Folded in at I133–I134**:
the subsection is Appendix C, Section `app:fc-split` (the report's "Appendix F" is C in this
build, as intended), and the body sentence after `prop:rc-lower` cites `prop:fc-split`.

## Final items launched (11-03, subagents, written incrementally)

- `audits/reviews/2026-11-03-rees-threshold-4.md` (DONE, negative): removing the degenerate
  configurations exactly beats T_A only at κ = 3. The missing ingredient is square-root bounds
  for sums that touch every row and column. Folded into `rem:two-level-threshold-size` at I135.
- `audits/reviews/2026-11-03-rees-circuit-3.md` (DONE): sparse coset-support mode
  (`theorems/rees_circuit_sparse.py`). It runs class four on n5(F_5) for 9 subgroups (6
  non-normal), all passing, and matches the dense mode exactly; the parent reran the fast
  tests, 20 passed. Folded into "Gate-level control" at I136, with the stated caveats: grade 2 is
  sampled, and grades 4 and 3 are exhaustive for two subgroups only.

## 11-04 afternoon checkpoint (parent)

- **I153 applied** (`audits/reviews/2026-11-04-rees-check-i149-151-r2.md`): two errors, two gaps,
  one borderline gap and most imprecisions of the unanchored I149–I151 check are fixed (see the
  log row). The build dir in the scratchpad had stale `.tex` copies; copy every `*.tex` there
  before `latexmk`. Clean: 125 pp., no overfull or float warnings. `pytest -q tests -k rees`:
  982 passed, 35 skipped.
- **Local subagents launched 11-04 ~12:45** (each writes its report incrementally; if a report
  is partial, continue it from its last section):
  - `audits/reviews/2026-11-04-rees-qft-wire.md`: `lem:qft-mod` as an optional backend in
    `theorems/rees_circuit_general.py`; new tests `tests/test_rees_circuit_qft_wire.py`.
  - `audits/reviews/2026-11-04-rees-coherent-sde.md`: reversible linear-grade SDE solve,
    `theorems/rees_coherent_sde.py`, `tests/test_rees_coherent_sde.py` (item 7).
  - `audits/reviews/2026-11-04-rees-threshold-5.md`: non-character-sum routes to the square
    gap (item 2).
  - `audits/reviews/2026-11-04-rees-lean-c5.md`: BCH group law at class five, new files
    `formal/Formal/BCHClassFive.lean` etc. only (item 8).
  - `audits/reviews/2026-11-04-rees-notation-table.md`: referee m1 notation table and symbol
    collisions.
  - `audits/reviews/2026-11-04-rees-referee-3-body.md` and `-referee-3-appendices.md`: unanchored
    referee passes on the main.tex body and on Appendices B–C (schedule3, free-coordinate). An
    error there outranks everything else.
- **I154 (notation table, referee m1)** is in: `sec:notation` with three tables, 128 pp., clean. The 40 symbol
  collisions in `audits/reviews/2026-11-04-rees-notation-table.md` §3 are NOT renamed (K32, owner or a later pass).
  Row-by-row check done (`audits/reviews/2026-11-04-rees-notation-verify.md`): 10 of 56 rows fixed, no formula wrong.
- **I155 (coherent linear-grade SDE solve)** is in: `lem:coherent-linear-sde` after "Gate-level control". It covers
  only κ_d = 1 grades (grade 2 always has κ = 2), is not wired in, and the gate stays false. Next for item 7: a coherent
  κ = 2 solve (the report's §6 suggests the triangular solver), then wiring a controlled merge on a witness register.
  **κ = 2 solve done** (`audits/reviews/2026-11-04-rees-coherent-sde-k2.md`, `theorems/rees_coherent_sde_k2.py`,
  `tests/test_rees_coherent_sde_k2.py`: 140 passed, 19 skipped, parent rerun): triangular solver made reversible, oblivious
  Tonelli–Shanks, explicit universal κ = 2 contraction (its Lemma 1), Lemma 4 simplification; exhaustive a = 2 at p = 3, 5.
  Class 2 now has a coherent SDE solve modulo wiring; class 3 only at p ≡ 2 mod 3. Its §6 lemma `lem:coherent-quadratic-sde`
  is in the paper (I160). Next: wire both coherent solvers into the merge (report §9).
  **Wiring done (I161):** `theorems/rees_circuit_coherent.py` gives a measurement-free receiver (until final Fourier
  sampling) on Heis(F_3) and n4(F_5); report `audits/reviews/2026-11-04-rees-circuit-coherent.md`. Gate stays false:
  only two instances, κ ≥ 3 classical, QFTs exact unitaries in that backend. Next: combine with the explicit-QFT
  backend (agent running: `audits/reviews/2026-11-04-rees-circuit-full.md`, `theorems/rees_circuit_full.py`), and κ ≥ 3 (agent running).
  κ = 3 coherent solve launched: `audits/reviews/2026-11-04-rees-coherent-sde-k3.md`, `theorems/rees_coherent_sde_k3.py` (target n4(F_7)).
- **Referee 3, Appendices B–C** (`audits/reviews/2026-11-04-rees-referee-3-appendices.md`): 1 error (a trial-cap prime),
  5 gaps, 22 imprecisions; no error in any probability bound. A subagent is applying it (backup `scratchpad/bak-i156`),
  with a per-finding table in `-referee-3-appendices-applied.md`; the parent then reviews and logs I156. Do not edit
  the appendices while that runs.
- **Lean class five done** (`audits/reviews/2026-11-04-rees-lean-c5.md`): `formal/Formal/BCHClassFive.lean`,
  `BCHClassFiveSubgroups.lean`, `ReesGeneralLawClassFive.lean`; no sorry, standard axioms only (parent checked
  `#print axioms` on the main theorems). The parent added the three imports to `formal/Formal.lean` and
  `formal/Formal/Audit.lean`, the 21 axiom guards to `Audit.lean`, and "c at least six" in `formal/README.md`
  (backups in the scratchpad). Paper sentence (report §6) to go into `sec:formalization` once the referee-3
  applier is done with the .tex files. Class six and up stays open.
- **QFT wired as an optional backend** (`audits/reviews/2026-11-04-rees-qft-wire.md`, `theorems/rees_circuit_qft_wire.py`,
  `tests/test_rees_circuit_qft_wire.py`, 11 tests). Pending paper edit (after the referee-3 applier): report §8 text in
  "Gate-level control", plus one proof sentence in `lem:qft-mod` that on input |0⟩ only the PREP error remains
  (parent-checked: rest of V acts exactly on |u_N⟩|0⟩, so the telescoping leaves only the PREP term).
- **Referee 3, body** (`audits/reviews/2026-11-04-rees-referee-3-body.md`): 0 errors, 1 gap (proof of `thm:main` uses
  `thm:is-import` at d ∤ p−1 without citing the Bezout reduction), 19 imprecisions (Bezout-lift wording contradicts
  itself, `thm:free-coordinate` hypothesis κ_d < p−1 vs part (iii), undefined `t` in Section 3, `tab:query-crossover`
  column rounding, abstract's Lean boundary now c ≥ 6). To apply after the appendix applier, then log I157.
- **I156 logged** (referee-3 appendices applied, 27/28; parent added per-node Phase 0 to `rem:app-s2-four`).
  **I157 in progress:** a subagent applies the body referee, the qft-wire §8 text with the zero-input proof sentence,
  and the Lean class-five sentence (abstract + `sec:formalization`); backup `scratchpad/bak-i157`; its table goes in
  `audits/reviews/2026-11-04-rees-referee-3-body-applied.md`. The parent then reads the diff and logs I157.
- **I157–I158 logged.** Body referee applied; explicit-QFT backend text and the zero-input proof sentence are in;
  Lean class five is in the abstract and `sec:formalization` (417 guards); the Bezout conversion is proved in
  `rem:is-import`(b) and no longer a condition. Owner/later items: B_d(0) at empty grades in `thm:main`; renaming the
  40 reused letters (K32); Dixmier–Lister rank rewording. Next: an unanchored check of the I153–I158 edits.
  `pytest -q tests -k rees` after I158: 1160 passed, 52 skipped (14 min). Check done
  (`audits/reviews/2026-11-04-rees-check-i153-158.md`): 0 errors, 1 gap (arithmetic blocks need Cuccaro et al. 2004,
  Vedral–Barenco–Ekert 1996), 14 imprecisions; all applied as I159 (table `-check-i153-158-applied.md`).
- **I162, threshold-5** (`audits/reviews/2026-11-04-rees-threshold-5.md`): analytic non-character-sum routes fail, but κ = 8
  now has an explicit certificate: no prime of (49417, 8^8/2] is in E_2(8) (139,558 independently checked witnesses).
  Appendix A's κ = 8, 9 sentence updated with scan data as of 11-04 ~15:00 (κ = 8 decided to 9649, 9473 ∈ E_2(8);
  κ = 9 decided to 12799, 17623 ∈ E_2(9)). Re-read the scans and update those numbers when they finish. Open: the 29
  primes in `2026-11-04-rees-threshold-5/gap_k8_unresolved.txt`; (8^8/2, T_A(8)] is a mechanical sweep (~10^5–10^6 CPU-s;
  a cloud job candidate). Do not commit the 27 MB sweep files or the binaries in that folder.
- **I163, coherent-sde-k3** (`audits/reviews/2026-11-04-rees-coherent-sde-k3.md`): `lem:coherent-power-sde` in main.tex makes the SDE solve coherent at every grade with p ∉ E_2(κ_d) (all class 3; class 4 for p ∉ {5,13,17,29,37,53}). Artifact `theorems/rees_coherent_sde_kappa.py`, tests `tests/test_rees_coherent_sde_k3.py` (87 passed, 27 skipped). Not wired: next step is a fifth backend run on the class-three filiform algebra over F_7 (κ_3 = 3).
- **I164, check of I159–I163** (`audits/reviews/2026-11-04-rees-check-i159-163.md`): all 14 findings applied except F6 (fifth backend, pending). Paper 134 pp. E_2(8) ∋ 9769, decided to 9769; κ = 9 decided to 12979. Open: an unpruned (nosym) rerun of the record primes 9769 and 17623 (F14).
- **I165, circuit-full** (`audits/reviews/2026-11-04-rees-circuit-full.md`): coherent + explicit-QFT circuit on Heis(F_3), n4(F_5) (`theorems/rees_circuit_full.py`, `tests/test_rees_circuit_full.py`, 11 passed), now in Gate-level control. Not simulated as a whole.
- **I166, circuit-coherent-k3** (`audits/reviews/2026-11-04-rees-circuit-coherent-k3.md`): fifth backend `theorems/rees_circuit_coherent_k3.py` wires lem:coherent-power-sde at κ_3 = 3 on filiform F_7; in the paper. Open: κ = 4 wiring: the smallest prime with κ_4 = 4 and p ∉ E_2(4) is 41, so a class-four instance has |G| ≥ 41^11, beyond exact simulation; only gate generation and per-block checks are feasible there.
- **I167, review of the fifth backend** (`audits/reviews/2026-11-04-rees-circuit-coherent-k3-review.md`): no errors; imprecisions applied; `run.json` regenerated; G2 tests added (22 passed, 1 skipped) (κ = 3 state check by default, coset-flag mutant, whole-sample emitted count 4832806).
- **I168, coherent class-four F_7** (`audits/reviews/2026-11-04-rees-circuit-coherent-c4.md`, `theorems/rees_circuit_coherent_c4.py`, tests 23 passed): every grade coherent on the class-four filiform algebra over F_7; in the paper. Review: `-circuit-coherent-c4-review.md` (I169: 0 errors; sentence replaced; source-check code fix applied, 30 passed).
- **I169–I171**: class-four review applied (0 errors) and its source-check gap fixed in code; E_2(8) ∋ 10321 (decided to 10433), E_2(9) ∋ 17659 (decided to 13537); referee-4 consistency pass applied across all files (`audits/reviews/2026-11-04-rees-referee-4-consistency{,-applied}.md`). Paper 135 pp., clean. G13 resolved as I172: (H2) discharged (`audits/reviews/2026-11-04-rees-h2-check.md`); only (H3), the Shor order-finding cost, remains a hypothesis of prop:tb-count-gates.
- **I172–I173**: (H2) discharged (only (H3) left; `-h3-check.md` agent running); `prop:coherent-receiver` added: a measurement-free receiver with the queries, arities and error of thm:main and explicit polynomial gates in terms of T^IS_d (existence; gates stay false). Next hard question: an explicit polynomial T^IS_d from Ivanyos–Santha §§3.1–3.3, and an unanchored check (`-coherent-receiver-check.md`, running). Paper 138 pp.
- **I174–I175**: (H3) discharged (explicit order finding, `-h3-check.md` Applied section), so all three hypotheses of prop:tb-count-gates are discharged; the coherent-receiver check (1 Error, 2 Gaps, 9 Imprecisions) applied in full: the Scope paragraph no longer claims an explicit polynomial count, the solver is a fixed machine 𝓜_d per (d, κ_d) reading p from tape, the reused workspace stays clean, the gate bound gains +4bQ. Paper 140 pp. Next: the IS runtime agent (`-is-runtime.md`) for an explicit T^IS_d.
- **Cloud jobs started by the owner on 11-04 afternoon:** `rees-cloud-zero-sum` (task_3087361b, a
  polynomial-time zero-sum finder at near-linear arity; result goes in
  `audits/reviews/2026-11-04-rees-cloud-zero-sum.md`), `rees-cloud-citations` (task_8de856b9; result goes in
  `audits/reviews/2026-11-04-rees-cloud-citations.md`) and `rees-cloud-dfs2b-k8-tail` (task_cf3ba4f9). All three
  report only in their final messages: open each in the app and copy the message into its file, checking it.
- **dfs2b κ = 9 on [5690, 11000] is complete** (`dfs2b_k9_5690_11000.out` + `dfs2b_k9_8462_11000.out`, DONE, limit=0):
  91 INFEASIBLE primes (in E_2(9)), 7 FEASIBLE (6607, 7489, 8821, 9001, 9397, 9883, 10369), largest infeasible 10909.
- **dfs2b rescans** still running in `screen` (see the midday checkpoint). At 12:40 the newest
  files had reached p = 7993 (κ = 8), 10531, 11863 and 14653 (κ = 9); 17501–20000 had no line yet.

## 11-04 midday checkpoint (parent)

- **dfs2b full rescans, running locally** (niced, 48 h cap), in
  `audits/reviews/2026-11-02-rees-schedules/small-prime/`: `dfs2b_k8_4202_20000.out`,
  `dfs2b_k9_5690_11000.out`, `dfs2b_k9_11001_14500.out`, `dfs2b_k9_14501_17500.out`,
  `dfs2b_k9_17501_20000.out` (started 11-04 11:49 local). Each line is
  `INFEASIBLE|FEASIBLE|LIMIT k=… p=…` for each prime p ≡ 1 mod κ in the range. FEASIBLE means a
  two-level contraction exists (p ∉ E_2(κ)), and INFEASIBLE means p ∈ E_2(κ). A finished file ends
  with `DONE k=… feasible=… infeasible=… limit=…`. A file without a DONE line was cut off:
  restart from the last prime it printed, `./dfs2b K P_last+1 P1 4000000000 print`. If DONE shows
  `limit=0`, E_2(κ) ∩ [P0, P1] is exactly the set of INFEASIBLE primes. Fold that into
  `prop:small-prime-arity` and `2026-11-02-rees-dfs2-complete.md`. E_2(9) still needs p up to about
  10⁵ (cloud item 11), so it stays incomplete either way.
- **Cloud jobs.** All four earlier jobs are now confirmed started: `rees-cloud-dfs2`
  (task_bc0a5c3f), `rees-cloud-linear-arity` (task_7f3dccf6), `rees-cloud-a1` (task_661dd95f)
  and `rees-cloud-dfs2-k9-high` (task_1914ebba), the last three on 11-04. A fifth was requested on
  11-04, after the owner said "remember to use cloud agents when possible":
  `rees-cloud-dfs2b-k8-tail` (task_cf3ba4f9). It runs dfs2b at κ = 8 on [20001, 60000], with the
  source pasted into the brief and checked against node counts from the local runs. Its result
  goes in `audits/reviews/2026-11-04-rees-cloud-dfs2b-k8-tail.md`. Cloud sessions report only in
  their final messages, which the parent cannot read. Copy each one into its file, checking it
  as you go.
- **Proposed cloud card (not started):** `rees-cloud-citations` (task_8de856b9). It checks
  all 40 pinpoint citations (theorem, section and equation numbers, plus the attributed
  claims) against their primary sources, including Lidl–Niederreiter 5.41 (K1/K14) and
  Khukhro. Results come only in its final message; copy them into
  `audits/reviews/2026-11-04-rees-cloud-citations.md`. Without the cloud, a local pass with
  network access can do the same job from that brief.
- I152 (`rem:fc-tradeoff`, from `-avg-case-arity.md`): the average case is negative. The
  remark records the hybrid trade-off of about κ^{a−K} trials at arity about Ka, and a
  lower bound for split nodes.
- **Restart, 11-04 12:00.** A session restart killed every local job. The rescans were restarted
  in detached `screen` sessions from the last prime each had printed. The new files are
  `dfs2b_k8_6362_20000.out`, `dfs2b_k9_8462_11000.out`, `dfs2b_k9_11162_14500.out`,
  `dfs2b_k9_14501_17500.out` and `dfs2b_k9_17501_20000.out`. The older files
  (`dfs2b_k8_4202_20000.out`, `dfs2b_k9_5690_11000.out`, `dfs2b_k9_11001_14500.out`) hold the
  primes done before the restart and have no DONE line. A range counts as covered when the old
  file plus the new one cover it.
- **Folded in on 11-04 (parent-checked, AI only):**
  - I149, `-mixed-rule.md`: `prop:mixed-schedule` in the new Appendix B subsection
    `app:s3-mixed`. It is a stated theorem for the uniform-kernel column of `tab:fcs-budget`,
    with a node-count-weighted bank budget. The column is reproduced exactly by an independent
    script. The unweighted rule fails at p = 151 (class nine).
  - I150, `-qft-mod.md`: `lem:qft-mod`, an explicit QFT over Z/N with O((b+log 1/η)²) gates.
    (H1) of `prop:tb-count-gates` is now proved, not assumed. Proof (b) of that proposition was
    fixed, because it still used the old count. The lemma is not wired into the generated
    circuits.
  - I151, `-zero-sum-node.md`: `lem:fc-zero-sum`, so `cor:fpt-r`(ii) at p = c+1 now holds
    through (iii) with the deterministic zero-sum node of arity g_c(p−1)+1. IMS is kept as the
    alternative that needs no label law.
- **Still running:** `audits/reviews/2026-11-04-rees-avg-case-arity.md`, an exploratory o(a²)
  average-case SDE attempt (a negative result is likely). Also
  `audits/reviews/2026-11-04-rees-check-i149-151.md`, an unanchored check of the I149–I151
  text. **Read the check first:** an error there outranks everything else.

If either file is incomplete, continue from its last section. The three cloud cards
(`rees-cloud-dfs2-k9-high`, `rees-cloud-linear-arity`, `rees-cloud-a1`) were requested on the
owner's word on 11-03. Their briefs are in `REES_FULL_CAMPAIGN_4.md`, items 10–12. No note comes
when a cloud session ends: open each one in the app, copy its final message into the output file
that row names, and check it before folding it in.

## Results landed in rounds 3 and 4 (checked by the parent at 11-02 ~22:00)

None found an error or counterexample.

- **Appendix F, free coordinate** (`appendix-free-coordinate.tex`, report
  `-free-coordinate-appendix.md`): proves `thm:free-coordinate` and `prop:rc-lower`, with the
  trial cap 2^33.78. Sent to the integrator together with the K7 merge decision.
- **Proof checks, round 4.** All verdicts hold; only gaps and text items were found. Each
  report's fixes were sent to the integrator. Check its log rows past I94 to see what was
  applied.
  - `-check-app-a.md`: G1–G3, D1.
  - `-check-app-b.md`: 9 minor items, plus "the label law is derived, not assumed". Applied
    at I106–I111. The qualifier change is logged separately at I112. P9 and P10 (optional) are
    not applied (K25).
  - `-check-app-e.md`: a five-dimensional counterexample to "class at most b".
  - `-check-core.md`: G1, the `lem:hybrid` domain mismatch with
    `thm:uniform-compilation`(iii), the most substantive; G2, N_instr undefined.
  - `-check-app-d.md`: no theorem-level counterexample; one false sentence (9a) and P7, the
    r_loc = 0 branch error. Folded in at I115, I116 and I118–I120.
  - `-check-app-c.md`: all lemmas hold. F1: the precision clause of `thm:app-sub-hsp` must be
    stated on the reachable domain (the same issue as check-core G1). Folded in at I117 on
    `lem:hybrid`'s convention, and the other items at I121–I122. P9 (optional) is open (K27).
    All six round-4 checks are done.
- **Lean-3** (`2026-11-03-rees-lean-3.md`): three `formal/Formal/ReesSde*` modules, built in
  place with `lake build --wfail` (3511 jobs, no clean clone). Its build log sits outside the
  repo in the app's side-session-notes, so rerun the build to regenerate it. In the paper
  at I123: 31 guards recounted from Audit.lean, and "in-place build" only. `formal/README.md`
  has had its section on these modules since 11-03 (K26, closed by the parent).
- **Mixed-source simulation** (`2026-11-03-rees-mixed-source-sim.md`): no counterexample on 61
  nonflat states, with negative controls (`theorems/rees_mixed_source_sim.py`). In the paper
  at I124 as an exact finite computation; the general step stays argued.
- **Core paper:** `docs/papers/rees-hsp/core/main-core.tex`, 25 pp. (report
  `2026-11-03-rees-core-paper.md`). Its session was asked to delete the build products in
  `core/` and to close check-core G1/G2. Verify that `core/` holds only `.tex`, `.bib` and
  `numbers.tex`.
- **Threshold-3** (`2026-11-03-rees-threshold-3.md`): no better threshold, but a proved
  obstruction. Term-by-term and (κ−1)-column character-sum arguments cannot certify any
  p ≤ κ^κ/2. Folded into `rem:two-level-threshold-size` at I113–I114.
- **Still running at this checkpoint:**
  - The cloud jobs, which report only in their final messages: `rees-cloud-dfs2`,
    `rees-cloud-dfs2-k9-high`, `rees-cloud-linear-arity` and `rees-cloud-a1`.
  - A missing output file means that item did not finish.

## What "full" still lacks (ranked)

1. **Human review.** This is the binding gate and cannot be done by AI. Everything else is
   AI-checked only.
2. **The Schedule 2 threshold gap.** The proved threshold is T_A ≈ (κ−1)κ^κ, with a
   central-moment bound κ^{κ+o(1)} that only helps for κ ≥ 15. The observed one is about
   1.5κ^{(κ+1)/2}, so the square gap is open (`-threshold-2.md` §5). E_2(κ) is exact for
   κ ≤ 7. For κ = 8, 9 the dfs2 scans (`-schedules/small-prime/dfs2_k8_*.out`) hit LIMIT at
   4153, 4201, 6073, 6089 and 8009, and κ = 9 above 5689 is unscanned. Next: a better
   pruning bound in `dfs2.c`, or a proof that closes the gap.
   Threshold-8 (`-threshold-8.md`, checked in `-threshold-8-check.md`, 11-05; in the paper as
   `app:s2-local` plus one sentence in `rem:two-level-threshold-size`): lower bounds only.
   Proved: a vanishing cyclotomic number A(u,v) gives a two-row obstruction, so every prime
   p ≡ 1 (mod κ) with p ≤ κ²−3κ+3 is in E_2(κ) (void above ((κ−1)(κ−2)+2)², κ ≥ 4);
   E_2(D) ⊆ E_2(κ) on p ≡ 1 (mod κ) for every D | κ (threshold-7 Prop. 4.6; the report's
   coprime-cofactor Lemma 5 is the special case); r-row obstructions are void above
   ((r−1)κ^r+2)². Computed (two codes): E2row(κ) complete for κ = 3..16; E_2(10) ∩ [3, 8191]
   = all but 3361, 3761, 5821; every p ≡ 1 (mod 12) up to 10453 is in E_2(12). The unfitted
   Poisson-orbit model (heuristic, not in the paper) predicts max E_2(κ) ≈ 1.3–1.6κ^{(κ+1)/2}.
   The square gap is still open.
   Threshold-9 (`-threshold-9.md`, checked and integrated in `-threshold-9-check.md`, 11-05; in
   the paper as `rem:app-s2-joint-moments` after `prop:app-s2-TA` plus one clause in
   `rem:two-level-threshold-size`): Weil-controlled joint factorial moments of several column
   counts plus a double Bonferroni give p ∉ E_2(κ) for p ≥ 6κ^κ + 1 when κ ≥ 729 (5.5κ^κ + 1,
   κ ≥ 1677), using TH2 Theorem 5 (cited, not in the paper) above √(8κ)κ^κ; so O(κ^κ) instead
   of κ^{κ+o(1)}. No such bracket certificate can go below κ^κ/2 (instance of the BGP barrier
   already in the paper). Nothing new for κ ≤ 27; T_A and the table unchanged; square gap open.
   Next: an interval cover for 30 ≤ κ ≤ 728 (report §5), or a κ-column statistic for Λ < 1.
3. **Efficient SDE finding at arity o(a²).** None is known
   (`-linear-arity.md`, "Still missing"). The triangular solver at (a+1)(a+2)/2 columns is in
   the paper as `prop:triangular-sde`. Adopting it in Rule W (K10) is the owner's decision,
   because it changes the quoted exponent 143 and the E_W values. Since I211,
   `rem:sde-worst-case` (AI-checked, pending human review;
   `audits/reviews/2026-11-05-rees-sde-worst-case-check.md`) shows the existence threshold is
   linear, 2a ≤ N(κ,a,p) ≤ κa (N(2,a,p) = 2a), so the gap is a search gap. A reserved-basis
   steered solver solves every bank in general position with ⌊(a+2)²/4⌋+a columns (O(a²/log a) at
   p ≥ poly(a)), with no randomness over the columns. General position needs p ≳ a²/4 and, for Rees
   labels, p ≫ C(M,a_d), so nothing in the tables, E_W or 143 changes. For arbitrary columns the
   question is still open: the stall/true-pool loss (report Q1, Conjecture 5).
4. **Schedule 3:** the free-coordinate theorem `thm:free-coordinate` and `prop:rc-lower` are
   now proved in Appendix C (`appendix-free-coordinate.tex`, label `app:free-coordinate`;
   AI-checked, pending human review), folded in at I87–I94. Since pass 7 (I112) both Schedule 3
   titles say the label law is derived in Appendix B (`lem:s3-law`), not "conditional on the
   label law". The guarantee covers the i.i.d. ideal supply only. Nothing is called
   unconditional, and the corollaries citing them stay conditional through Thm main. Optional
   Appendix B/C polish P9/P10 is open (K25). K7 (K23): **merged** on the owner's decision
   (Schedule 3 integrator, 11-05, `audits/reviews/2026-11-05-rees-s3-integration.md`). The old
   `thm:random-column` is now part (iv) of `thm:free-coordinate`, still proved in Appendix B;
   part (ii) supersedes its trial count, and the label `thm:random-column` no longer exists. The block-splitting sentence after `prop:rc-lower` is now proved in
   Appendix C, Section `app:fc-split` (I133–I134). Since I221, `rem:fc-witness-h3` gives a
   weight-doubling node at every free-coordinate grade (digits μ_h ∪ {0}, depth j*_h ≤ ⌈log₂κ⌉,
   j*_h = 1 once √p > (κ−1)(κ−2)+3, j*_h = log₂p/φ(h) + O_h(1) for fixed h; arity of degree
   1 + j*_h in g_d, time poly(M_d, κ_d, log p), abort ≤ τ, i.i.d. supply only; no novelty
   claimed). With it the classical time of (iii) is polynomial at fixed c for every p > c, at a
   larger query count (exponent of m ≤ 19 at c = 9 up to log factors; log₂Q 93–151 against
   34–42 for the FCS nodes on the class-nine profile). One sentence after thm:free-coordinate
   says so; it is not adopted in (R1) and changes no table, E_W or numbers.tex (adoption is an
   owner decision; `2026-11-05-rees-s3-witness-h3.md`, check `-check.md`). The 'arity a + O(1)'
   question after prop:rc-lower is unchanged: the report's 'negative answer' holds only where the
   question is vacuous (h < κ^{o(a)}), and its replacement question (F2) is answered by a collision
   search when h ≤ κ^{1−Ω(1)}, so F2 was not applied (rewording is an owner decision). Still
   open: degree bounded uniformly in p for fixed h ≥ 3, and a zero-sum node at κ = p−1 with
   arity and time f(p)·poly(g_c), or arity o(g_c²) at fixed p. Since I210, `rem:fc-zero-sum-arity` gives a
   polynomial-time node at Γ_0 of arity O_c(g^{1+⌈log₂c⌉}·log(1/τ)), abort ≤ τ, i.i.d. supply only
   (KMOSW's affine-reducibility step at every weight level; no novelty claimed), with barriers for
   disjoint merging, switch recursion (Ω(n²/log n)) and oblivious information sets; it is not in
   (R1) and changes no table (`2026-11-05-rees-s3-arity.md`, check `-check.md`; AI-checked,
   pending human review). Adopting it in (R1) is an optional owner decision. At the grades with h = (p−1)/κ_d ∈ {1, 2} the
   node is average-case binary or ternary SIS, in both directions (`2026-11-04-rees-s3-zero-sum.md`
   Z1, A5; paper `rem:fc-zero-sum-sis`). A polynomial-time node at arity ≤ p²g^{−2δ} on primes
   p = Θ(g^k), k > 1, would approximate worst-case lattice problems within polynomial factors
   (Z2, via Micciancio–Peikert 2013 Thm 1.1; numbering and bib details NEED HUMAN
   VERIFICATION). But Schedule 3 has at least 2^{c−1} queries, so it can be polynomial only
   for p = O(log m), where that bound is silent (Z3; remark part (d)); the question that matters
   is f(p)·poly(g_c), or the fixed-p exponent. Literature nodes at Γ_0 reach (g+1)^{p−1}
   columns worst case and g^{1+⌊(p+3)/4⌋} on average (KMOSW, unverified; Z4), against
   B_{p−1}(g) for Schedule 1. The i.i.d. supply itself is produced exactly by the procedure
   (A2, A3), and the coset-copy extension of `thm:free-coordinate` is proved (A4; now stated in
   the theorem). AI-checked, pending human review. The zero-sum grade p = c+1 of the derived-dimension corollary is done at I151, with a p^{O(g_c)} search. The mixed uniform-kernel rule is a theorem at I149. The `tab:fcs-budget` artifact and the corollaries at every prime are done at I145.
5. **Appendix fixes for the owners' items:**
   - Lidl–Niederreiter Thm 5.41 (Appendix A, Weil bound) is still unchecked. The text says so;
     it needs the book.
   - K1: the Khukhro theorem number. It needs the book.
   - Pass-3 open items K19–K21 (integration log): the circuit report's unfilled placeholders,
     its run JSON outside the repo, and the untracked e2e-scale run JSONs that the
     `\ReesScale…` macros read (commit them with `numbers.tex`).
   - Optional round-4 polish not applied, all for a later pass or the owner: K25 (Appendix B
     P9, the sharper moment bound; Appendix C P10, renames), K27 (subspace appendix P9, the
     smaller product design with M ≤ 1890 at c = 9). K26 is closed: `formal/README.md`
     now has the ReesSde section and lists the three files.
   - Not folded in yet: dfs2 κ = 8, 9 (#4), waiting for its result.
   - K30 (owner's call): "Gate-level control" now says the instrument exponents are float-derived
     and rounded (error 7.5e-14); drop the clause if that check counts as exact.
   - Referee-2 items open for the owner (K29): status tags and one status convention (P3);
     remarks that state report-only results as facts (P6: rem:two-level-threshold-size and
     rem:triangular-scope done at I141; rem:premature, rem:mixed-source left, already labelled); repository and artifact pointers in
     place of `\file{}` (P7); terminology (P8); P11 (E_2(7) fixed at I138; G(d,a) defined and plain \input at I142; integrator comment lines in the appendix sources remain); prop:black-box (§2.4: done; the chart count of (iv) is proved as `lem:tb-chart` at I143); and the changelog. (q_max in the
     paper, §2.7, is done at I139.)
6. **Referee items not applied** (integration log, "Referee items not applied" and pass 4).
   Done in pass 4: M4 (body definitions of the two-level construction, contraction, E_2, T_A,
   T_S, fair-bit sampling, m_+, q_+, E_W; I79–I82), m3 (Dixmier–Lister derivations printed,
   I83), m9 ("exactly" kept with its derivation, I84) and m11 (artifact paragraph moved to
   §9.2, I85). Still open, all structural or for the owner:
   - F1: the restructure into core plus outlook.
   - Minor items m1 (notation table), m4 (cut Prop 2.6), m5–m7 (move tables, filters and Lean
     bookkeeping), m8 (retitle), m10 (IMS theorem number), m14 (Khukhro, = K1).

7. **Coherent receiver.** The gate stays false. A general gate-level generator now exists
   (`theorems/rees_circuit_general.py`, `-circuit-2.md`; in the paper's "Gate-level control"
   paragraph at I132). It is simulated exactly at c = 2 (Heis(F_3), gate for gate equal to the
   old circuit) and c = 3 (n4(F_5): 9 subgroups, 5 non-normal, 18/18 recoveries; n4(F_7)
   sampled) and, in the sparse mode of `theorems/rees_circuit_sparse.py` (`-circuit-3.md`, I136),
   c = 4 (n5(F_5): 9 subgroups, 5 non-normal (corrected 11-04 from 6), one recovery each; grade 2 sampled, grades 4 and 3
   exhaustive for two subgroups). n5(F_7) is generated and counted, not simulated. Still missing:
   - poly(log p) arithmetic: done at I146 (`theorems/rees_circuit_arith.py`, O(log² p) gates per
     multiplication); a poly(log p) QFT over Z/N is now `lem:qft-mod` (I150), and it is wired into an optional third backend, `theorems/rees_circuit_qft_wire.py` (I157, `-qft-wire.md`; done, not open);
   - a coherent SDE solve (partly done: coherent linear, quadratic and power SDE lemmas and circuit backends at I155, I160, I163, I166; read main.tex "Gate-level control" for the current coverage before working on this); it was classical between quantum segments, at Chevalley–Warning
     arities, with exhaustive search below the solver's column count;
   - exhaustive class-four merges, n5(F_7) or class five, and a monolithic (not module-by-module)
     simulation: partly done 11-05 (`audits/reviews/2026-11-05-rees-receiver-sims.md`, checked in
     `-receiver-sims-check.md`, no Error; paper text at I208). Monolithic
     sampled-trajectory simulation of the coherent terminal sample (`theorems/rees_circuit_mono.py`):
     Heis(F_3) all 19 subgroups (fully coherent, level 0, for 6 of them), n4(F_5) 7 of 9. Exhaustive
     merges (`theorems/rees_circuit_exhaustive.py`) for n5(F_5) (all 9, gate-list source), n5(F_7)
     (8 of 9) and n6(F_7) class five (7 of 8) by exact checks (E1)-(E3) plus a five-line argument (R)
     that is argued, not machine-checked.
     Round 2 (11-05, `audits/reviews/2026-11-05-rees-receiver-round2.md`, checked in
     `-receiver-round2-check.md`, no Error; paper text at I212), done:
     - exact output law (level 0, = the trajectory average) of the whole Heis(F_3) circuit for all
       19 subgroups (hub decomposition over labels and Q), uniform on h^perp; this covers the 13
       small-S subgroups;
     - checkpoints K0-K5 at c = 2 against references computed from h (K4 relative to the split):
       92 mutant runs, 72 caught, 20 with the dropped gate never firing (state identical), none
       missed; per-source checkpoint KS in the trajectory mode at c = 2 and c = 3;
     - step (R): the product identity is Lean-checked in `formal/Formal/ReesMergeReduction.lean`,
       now an audited module (I218, 11-05: imported by `Formal.lean`, 5 `Audit.lean` guards, row in
       `tab:lean-modules`, in the guard counts; check `audits/reviews/2026-11-05-rees-lean-sde-solver-check.md`);
       the tie "merge output = function of the product" is still code reading;
     - seeded runs at class five, n6(F_7): 14/14 (complete power-class search, 3^10 points at grade 3).
     Still lacking:
     - a machine-checked tie of (R) to the merge code and to the gate-level
       circuit (the audited Lean module for (R) itself is done, I218) (the merges are the Schur-product channel, not a gate-level simulation at class four/five);
     - any level-0 (exact-law) run at c = 3 (needs re-merging hub branches: the grade-2 Q is a QFT
       target of its own instrument); the two largest n4(F_5) subgroups (gamma_2, <e1+e2,e3>;
       4.9e7-row factor); deterministic merge checkpoints at c = 3;
     - gate-list sources on all addresses and any gate-level simulation at p = 7 and class five
       (F_7 sources are the coset density computed from h, so F_7 recoveries test the descent only);
       gamma_2 of n5(F_7) and gamma_4 of n6(F_7); coherent-label (kappa >= 3) circuits at class five;
     - the explicit QFT of lem:qft-mod inside the monolithic simulation; a coherent receiver for
       general (G, H) (gate `coherent_receiver_implemented` stays false).
   Fixed at I137: the label at `theorems/rees_end_to_end_sim.py` line 924 (and in `_ext.py`)
   now reads "<e2,e3> non-normal"; 83 tests pass. Archived run JSONs keep the old string.
8. **Lean beyond c = 7:** the BCH/Lazard group law for c ≥ 8, solvers for κ ≥ 3, running
   times and arity bounds. These are outside the boundary (`-lean-2.md` §5). Solvers at κ ≤ 2
   are now in the default build (I218, 11-05, `ReesSdeSolver`, report `-lean-sde-solver.md`,
   check `-lean-sde-solver-check.md`): computable Gaussian elimination, the triangular solver
   with the contraction as input (`triSolve_spec`, (a+1)(a+2)/2 columns, any field), κ = 2
   over ZMod p with no input but p, d and the columns (`quadSolveZMod_spec`), κ = 1 at a+1
   (`linSolve_spec`), exhaustive Chevalley–Warning search at κa+1 (`cwSearch_witness`,
   `cwSearch_zmod_gcd`); running time unproved (square roots by O(p) search, exhaustive search
   p^M); not wired into the receiver policies of `ReesSdePolicy`. Class five (11-04, `-lean-c5.md`),
   class six (11-05, `-lean-c6.md`) and class seven (11-05, `-lean-c7.md`, checked in
   `-lean-c7-check.md`, integrated I217) are in the default build: septic BCH group over any
   field with 2, 3, 5, 7 ≠ 0; every subgroup over ZMod p, p ≥ 11, a Lie subalgebra; tuple
   hiding and measured terminal source at c = 7 (SDE policies remain inputs; no class-seven
   `ReesSdePolicy` instance). Guards (after I218: `ReesSdeSolver` 24, `ReesMergeReduction` 5) 500 for
   `tab:lean-modules` + 38 unrelated = 538 (`grep -c "#print axioms" formal/Formal/Audit.lean`).
   Full in-place `lake build --wfail` passed 11-05 after I218. Open: a
   clean-copy `lake --no-cache build --wfail` (BCHClassSeven alone took ~1 h 44 min wall in
   place) and human review. Machine-checked in Lean; AI-run, pending human review.
9. **Native application:** none (round 1 `-application.md`, negative). Without one,
   `speedup_claim_allowed` stays false. The classical query bound Θ(p^{(m−1)/2})
   (`prop:classical-query`) gives a query separation only, conditional on Thm main.
   2026-11-05 application-4 (`audits/reviews/2026-11-05-rees-application-4.md`, checked in
   `-application-4-check.md`, integrated I214): Theorem W, the Lie method on the Weil
   restriction R_F, computes the S1 stabilizer classically when p > max((ν−1)δ̂, 2δ̂) for a
   known p-weight bound δ̂ (bounded δ̂: Luks, every p > δ̂). The S1 residual now needs unbounded
   p-weight ≥ p/max(ν−1,2) or superpolynomial, and for fixed D a superpolynomial p. Still no
   application; possibly known, NEEDS HUMAN VERIFICATION.
10. **A1 novelty:** "possibly new". Three Google Scholar citers are unidentified
    (`-a1-citers.md`).

## Next command and acceptance test (top item a Codex pass can do)

Item 2. In `audits/reviews/2026-11-02-rees-schedules/small-prime/`, read `dfs2.c` and add a
stronger infeasibility prune. Then rerun only the LIMIT primes, for example
`./dfs2 8 4153 4153 50000000`. Save the output as `dfs2_k8_rerun_<p>.out`.
**Acceptance:** every LIMIT line is resolved to INFEASIBLE or FEASIBLE, with a cross-check by
an independent method on two primes. Record the largest infeasible prime per κ in a new
`audits/reviews/2026-11-0X-rees-dfs2-complete.md`.
