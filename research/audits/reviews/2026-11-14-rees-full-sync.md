# Rees full version synced to the core snapshot (2026-11-14)

AI-run (Claude), pending human review. This is editorial integration only: no new
mathematics was written, apart from the Lean-finding convention fixes in section 3. The
source of truth is `research/audits/reviews/2026-11-14-rees-full-sync/core-snapshot-68pp.tex`,
which is identical to `docs/papers/rees-hsp/core/main-core.tex`. The core file was not
touched, `make_numbers.py` was not run, and no Git commands were used.

## Verdict

**DONE.** The full version (`docs/papers/rees-hsp/main.tex` plus its appendices) is now a
superset of the snapshot:

- All 95 snapshot labels are mapped: 27 SAME, 24 ADAPTED, 2 STRONGER, 42 ADDED, **0 MISSING**.
  See `2026-11-14-rees-full-sync/superset_map.md`.
- The build is clean, at **276 pages** (the pre-sync baseline is 230).

There is one deviation from the brief: the new macros are defined in `main.tex`, not in
`numbers.tex` (section 4).

## 1. What changed

Backups:

- The pre-sync full version is in
  `research/audits/reviews/2026-11-09-rees-paper-pass-prep/backup-full-pre-sync-2026-11-14/`.
- The integration scripts are in `2026-11-14-rees-full-sync/scripts/`:
  - `integrate.py`, which uses anchored, uniqueness-asserted replacements and is not
    idempotent;
  - `make_core_appendices.py`;
  - `make_superset_map.py`;
  - the diff tools `envdiff.py`, `blockdiff.py` and `sentmiss.py`.

### `main.tex`

**Preamble** (l. 55–60):

- `\ReesClassNineHalvedExp` is 38 and `\ReesClassNinePlusExp` is 20.
- `\fullv` is defined as "this version".
- `\cl` is defined.

**Headline exponent.**

- The status quote, abstract, contributions, organization, related work, "What is new",
  Proof Overview and Verification Status now carry the headline 20 at c = 9, through
  Schedule 1H+. They also give 38 (1H alone), 53 (Schedule 1 alone) and 145 (full depth).
- `thm:main` (l. 248) is the snapshot statement, with arity `A^+_d` and both explicit bounds.
  `eq:Bd` was moved before it.
- `rem:main-solver` (l. 277) is the snapshot text, plus the full version's other solvers.
- Regimes table: there is a new Schedule 1H+ row. The caption notes were moved into a
  paragraph before the table, to fix a float-too-large problem that was already present
  before the sync.

**Ported from the snapshot:**

- `sec:prelim` (with `lem:fourier`), `lem:lifted-source`, `lem:instrument` and the Terminology
  paragraph;
- `lem:bezout`, `rem:zero-sum`, `rem:is-printed`, `cor:approx` and `rem:proof-uses`;
- the Heisenberg example `sec:example`, `rem:free23` (l. 361), `sec:status` and
  `sec:outlook`;
- the acknowledgements, including the draft **"Use of AI"** paragraph (l. 2333). This
  paragraph is draft text and needs owner editing.

**Schedules.** The snapshot's `sec:halving` (l. 981) and `sec:plus` (l. 1110) are inserted
before Schedule 2, with all lemmas, tables, proofs and certificates. The old
`rem:halving-core` (l. 1407) is rewritten. It now says:

- the full-version results that use Schedule 1, 2, the combined rule or 3 remain valid,
  since `A^+ ≤ A ≤ B`;
- combinations of those schedules with 1H/1H+ are not claimed.

**Merged remarks.**

- `rem:is-import` merges snapshot items (a), (c) and (d) with full-version items (b), (d)
  and (e). Every old reference to "(c)" now points to `rem:is-printed`.
- `rem:oblivious` and `rem:query-separation` are merged the same way. The sentence that the
  `% NEEDS HUMAN VERIFICATION` comment had swallowed was claimed here to be printed on its
  own line. **That claim was wrong:** the sentence was still inside the comment. Round 2
  fixed it (Round 2, A4).

**Other main-text changes.**

- The class-three example stages are now the snapshot text.
- `tab:query-crossover` now holds the 1H+ values. The old table is kept as
  `tab:query-crossover-s1` (l. 1842).
- The "steps behind Theorem main" paragraph now names Schedule 1 plus the `sec:recursion`
  budget for the other results.
- There is a Lean-section placeholder for `Formal.Schedule1HPlus` (l. 2218–2220,
  `% INTEGRATOR` comment). The integrator should finalize it.

**Remark on the plus-section referee.** The merged write-up of `sec:plus` is described as
refereed in `2026-11-14-rees-core-plus-referee.md`, with verdict CORRECT WITH FIXES and all
fixes applied. The text also says that no human has read it.

### New appendices

- **`appendix-core-artifacts.tex`** (`app:artifacts`). This is the snapshot's artifacts list,
  adapted to this version.
- **`appendix-core-proofs.tex`** (`app:core-proofs`). It holds the snapshot's self-contained
  proofs of `cor:black-box` and `cor:black-box-pe`. The full version keeps its own proofs too.
- **`appendix-free23.tex`** (`app:free23`, 365 lines, about 10 pp.). This is Theorem HSP23,
  written by a helper agent from the free23 notes; see its
  `2026-11-14-rees-full-sync/free23-appendix-notes.md`. It is headed AI-proved and
  AI-refereed only, pending human review. It is conditional on IS Cor. 8, abelian HSP and
  exact QFT_p, and it is "not used elsewhere".

### `appendix-provenance.tex`

The heading of the `prov:bb-subspace` item was reworded to fix an overfull box that was
already present before the sync.

## 2. Compile

The build ran from `docs/papers/rees-hsp` as pdflatex ×2, bibtex, then pdflatex ×2:

- 276 pages;
- 0 `!` errors;
- 0 undefined references or citations;
- 0 multiply-defined labels;
- 0 overfull boxes;
- no float warnings.

`pytest tests/tools/test_rees_paper_numbers.py` gives 2 passed.

**Correction (Round 2).** The round-1 build was not fully clean. Two pdfTeX warnings
("destination referenced but does not exist") came from `f23:types` and `f23:alg`. See
Round 2.

The pre-sync baseline gave 230 pages, 0 undefined references, 1 overfull box and 1 float
warning.

## 3. Lean findings applied

These come from `2026-11-14-rees-lean-schedule1hplus.md`, as the coordinator requested.

1. **Representatives in the "Classes" paragraph** (l. 1116). A new sentence says that
   `ξ^m` with `m ∈ Z_D` uses the representative in `{0,…,D-1}`, used consistently in the
   preprocessing and in the run. The duplicate in "Multi-level contractions" (l. 1201) now
   points back to it.
2. **Certificate folder in `app:artifacts`.** The text now names `2026-11-13-rees-headline-below-38/`
   as "the draft folder" for the certificate tables. I checked on disk that
   `certs_stage1.json`, `tierB_witnesses.json`, `verify_all.py`, `thresholds.py` and the
   `v2/` files are all there.
3. **`cor:plus-chain` hypothesis** (l. 1151). It is weakened from `Δ_t = lift` to `Δ_t ⊇ lift`.
   The proof is "induction with `lem:plus-refine`", whose hypothesis is `⊇`.
   - This is now a deliberate difference from the frozen snapshot, and the core still
     says `=`.

## 4. Deviations and residuals

- **Macros in `main.tex`, not `numbers.tex`.** Hand-adding them to `numbers.tex` breaks
  `test_rees_numbers_tex_is_up_to_date`, because that test requires `numbers.tex` to equal
  the `make_numbers` render. `numbers.tex` was therefore restored byte-identical.
- **`\bigcup` became `\cup`.** `\bigcup` is not in the test's KNOWN command list. The full
  version already used `\cup` in `lem:rounds`.
- **Older equivalent wording was kept** where the full version has its own form. This
  covers:
  - the Dixmier–Lister paragraph;
  - the recursion and arity paragraphs;
  - the proof of `thm:uniform-compilation`, whose full statement is STRONGER;
  - the inline proof of the classical bound, where `app:classical-proof` maps to
    `sec:classical-query`.
- **The class-nine profile paragraph is still Schedule 1** (l. 1678: exponent 53 from
  `rees_hsp_reduction.json`). It is labelled as Schedule 1, but the profile was not
  regenerated, because `make_numbers` is forbidden.

**Helper-agent findings on HSP23** (advisory):

- the small-p bound `s(p)` rests on an outline-level derivation (Lemma E, step 6), which is
  flagged for human review in the appendix;
- "about 4200" copies is about 4206;
- the sign conventions for `D_ℓ` differ between the notes;
- a lighter import (Bacon–Childs–van Dam for constant dimension) might suffice, but this was
  not checked.

## 5. Adversarial self-check

- **Two budgets.** `sec:recursion` gives the Schedule-1 budget, and the snapshot's 1H+
  budget sits in `sec:main-proof`. The "steps behind" paragraph assigns the first to the
  other results. A reader could still mix them up, and a human should check that no
  full-version result silently cites the 1H+ count.
- **Black-box corollaries** still state counts with `B_d`. That is valid since `A^+ ≤ B`.
  - `rem:black-box-scope` (full version) says "Schedule 1 alone".
  - The snapshot proofs in `app:core-proofs` use Theorem main's solver.
  - Both are consistent, but the two proofs coexist.
- **Notation.** The snapshot writes the dilation `δ_θ` and the full version writes `δ_λ`.
  - The ported labelled environments use `λ`.
  - The ported intro paragraph "Central descent and gradings" (main.tex l. 145) keeps `δ_θ`,
    because `λ` denotes labels there. The full version's own Dixmier–Lister text (l. 655)
    also used `δ_θ` before the sync.
  - In `sec:halving` and `sec:plus`, `θ` is a different variable.
  - The mix is cosmetic but visible.
- **Structure.** The paper now has both a "Notation" and a "Preliminaries" subsection, and
  some overlap between them is likely.
- **HSP23 appendix.** It was written by a helper agent, and I checked only its status
  labels, its compile and one sentence. Its mathematics has had no check in this pass beyond
  the earlier AI referee.
- **Coverage check.** The superset check is by word and sentence coverage. It does not
  prove semantic equivalence of the ADAPTED rows.
- **Excluded claim.** I wrote no claim that the theorem holds without the IS import at c ≤ 9.
  Ivanyos is cited only for the full-depth bound fix (main.tex l. 278, 388, 872;
  provenance l. 45).

## Round 2 (2026-11-14)

AI-run (Claude), pending human review. The round followed the integrator's brief, in parts
A–D. It touched only these files:

- `main.tex`;
- `appendix-*.tex`, including the new `appendix-classical-proof.tex`;
- the sync folder.

`core/`, `numbers.tex` and `make_numbers.py` were left alone: `numbers.tex` is byte-identical
to the backup. There were no Git commands. The scripts are `2026-11-14-rees-full-sync/scripts/round2.py`
(parts A, B and D) and `round2c.py` (part C). They use anchored, uniqueness-checked replacements
and are not idempotent. The pre-round-2 copies are in the session scratchpad.

**Verdict: DONE.**

- Build: 281 pages, 0 errors, 0 undefined or multiply-defined labels, 0 overfull boxes, no
  float warnings, no pdfTeX destination warnings, bibtex clean.
- `test_rees_paper_numbers.py`: 2 passed.
- Superset map (regenerated): 24 SAME, 22 ADAPTED, 6 STRONGER, 43 ADDED, 0 MISSING.

### A. Full-sync referee findings (`2026-11-14-rees-full-sync-referee.md`), applied as worded

1. **Coherent receiver is a Schedule-1 result.**
   - All seven edits are applied: the abstract, l. 1565/1567/1569/1571/1604, and
     `appendix-backends.tex:47`.
2. **Solver of the black-box corollaries and combined-rule comparisons.**
   - All edits are applied, covering the abstract, the regimes table, l. 320, related work,
     `rem:black-box-scope`, the `cor:black-box-pe` lead-in, the bb-envelope paragraph and
     theorem, and the outlook.
   - Two lead-in sentences with the same error, which the referee did not list, are fixed the
     same way: before `cor:black-box` and before `cor:black-box-pe`.
   - The core copy of the outlook sentence is left to the integrator.
3. **Compilation preamble and inverse-transform bound.**
   - (a) Snapshot l. 1018 is restored verbatim before `lem:hybrid` (l. 807).
   - (b) The definition of C and J is added in `thm:uniform-compilation`(iii).
   - (c) The inverse-transform sentence follows the proof (l. 1497). It adds "Write
     F = QFT_p in (iii)", because the snapshot leaves F undefined.
   - (d) The map row is now ADAPTED.
4. **`rem:query-separation`.** The swallowed sentence now prints on its own line; pdftotext
   confirms it. The integrator's l. 1864 sentence was replaced by a statement about the bound:
   - the count depends on p;
   - it is at most `C^+_c c (m+τ)(m+1)^{E_+(c)-1}` (Thm main(4));
   - that bound is polynomial in m of degree up to E_+(c) and independent of p once p ≥ 3/ε;
   - no optimality claim is made.
5. **Stale "Theorem main uses B_d / deterministic Schedule 1".** All seven edits are applied
   (main.tex and three appendices).
6. **Notation table.**
   - The E_1 row now says "Schedule 1 bound".
   - Rows were added for A_d and A^+_d, and for E_H, E_+ and C^+_c.
   - The table's `\arraystretch` went from 1.08 to 1.04 to avoid a float-too-large warning.
7. **Lean placeholder.** See D.
8. **HSP23 appendix.** Sub-items 8.1–8.5 are applied as worded:
   - s(7) ≥ 0.279 and s(11) ≥ 0.480;
   - the "for every p" step-6 wording;
   - "a sketch… did not re-derive it";
   - a status/hypothesis prefix on `f23:route`;
   - a new import (I5) for the Lazard correspondence, with (I1)–(I5) at l. 5 and l. 34.

   All of 8.6 is applied:
   - the τ-coefficient wording;
   - the global D_l sign, which does not affect uniformity;
   - "the 300 runs of e2e_spoiled.py at p = 5";
   - "(route (c) not simulated on trivial H)";
   - the pointer to `f23:approx`;
   - the gate error renamed to ε_g.

Also applied:

- **Finding 9.** `\phantomsection` was added before `f23:types` and `f23:alg`, and also before
  `f23:branch` and `f23:W`. Those two became dangling once the appendix letters shifted.
- **Finding 12.** Done.

Not applied:

- **Finding 10** (θ/λ notation sweep). It is editorial and outside findings 1–8.
- **Finding 11.** It requires editing the test file, which I do not own.

### B. Ivanyos–Santha-free material (`2026-11-14-rees-is-free/`, referee PROVED WITH FIXES)

Inserted:

- **`lem:plus-free-const`** (l. 1327).
- **`thm:plus-free`** (l. 1336). It replaces the old `rem:plus-is`, whose label is kept as an
  alias.
- **Remark "Class ten and beyond"** (`rem:plus-free-ten`, l. 1364). It includes the F9
  sentence (q = ξ^5, at most 13 Las Vegas tasks).
- **Proposition "The case c ≤ 9 of Theorem main"** (`cor:main-free`, l. 1746, F2). It has a
  pointer at the end of "Correctness of the ideal procedure".

Edits E2–E9b and E12–E14b were applied verbatim, since their anchors occur in the full version.
These were re-anchored:

- E1 (abstract);
- E10, as F5 wording after the full version's plus-referee sentence;
- E11, as item (f) after the full version's item (e);
- R2, before the full version's "Cost on arbitrary oracles" remark;
- E15 (in `appendix-core-artifacts.tex`).

Referee fixes F1–F12 are all applied:

- **F3** uses the full version's wording ("conditional on [IS15, Cor. 8], which rests on their
  Theorems 3 and 5").
- **F7** weakens the hypotheses of `cor:black-box`, `cor:black-box-pe` and `cor:nilpotent` to
  c ≥ 10, and of `cor:utz` to n ≥ 11.
- **F8** is applied.
- **F4** replaces the status chain.

Sentences found only in the full version were made consistent in the same way:

- the status quote;
- the regimes-table notes;
- three sentences at l. 320;
- two items of the contributions list;
- the abstract's black-box clause.

Two judgement calls:

- **κ = 10 remark.** "two programs" is now "three programs, the third written by the referee",
  because the referee's `kappa10_ref.py` is a third independent program.
- **Status labels.** "AI-checked, pending human review" is added to the three new titles.

Not changed: `thm:bb-envelope` and `prop:coherent-receiver`. Both still assume the import,
correctly, because they use Schedule 1 or 2.

### C. Pointer gate (slimmed core → full version, by title)

| core pointer | full-version target | action |
|---|---|---|
| appendix "Proof of the Classical Query Bounds" | new `appendix-classical-proof.tex` (`app:classical-proof`) | **moved** `lem:collision` and the proof of `prop:classical-query` there; pointer left in sec:classical-query |
| paragraph "Direct twists beyond class two" | main.tex, paragraph in sec:intro | exists |
| lemma "The exponent of Schedule~1H$^+$" | `lem:plus-exponent` | exists (title plus status suffix) |
| lemma "The exponent" | `lem:exponent` | exists (title plus status suffix) |
| lemma "The halved exponent" | `lem:halved-exponent` | exists (title plus status suffix) |
| proposition "Central scalars of $\mathcal{L}_{\mathrm{DL}}$" | `prop:dl-central-scalars` | exists (title plus status suffix) |
| remark "The grades at the maximizers" | `rem:plus-profile` | exists |
| remark "A cover-free algorithm for the free class-three group" | `rem:free23` | exists |
| remark "Class ten and beyond" | `rem:plus-free-ten` | added in B |
| remark "The printed bound" | `rem:is-printed` | exists |
| section "Classical Query Complexity" (with its table of query counts) | `sec:classical-query`, with `tab:query-crossover` | exists |
| section "Black-Box Groups and Other Presentations" | `sec:black-box` | **renamed** from "Black-Box Groups and Flat Subspace Sources". The presentations paragraph moved in as its first subsection, "Presentations That Give an Explicit Chart" (`sec:presentations`), as in the snapshot. "Flat Subspace Symmetry Sources" (`sec:subspace`) became its own section. One provenance pointer was updated. |
| section "A Non-Gradable Example" | `sec:dixmier-lister` | **renamed** from "The Dixmier–Lister Non-Gradable Control Family". It is a subsection, as in the core. |
| Related Work | `sec:related` | exists |
| ancillary file `anc/rees-hsp-full.pdf` | `docs/papers/rees-hsp/arxiv/METADATA.md` l. 9 | matches |

METADATA l. 7 still says "68 pages" for the core. That is a read-only file, so this is for the
integrator.

### D. Lean section

The placeholder (l. 2239) is replaced, based on
`2026-11-14-rees-lean-schedule1hplus.md`. The new text says the package:

- has seven modules and 52 guarded declarations;
- checks the correctness of:
  - the refinement chains (`lem:plus-refine`, `cor:plus-chain`);
  - the two-class stage and finish;
  - the tensor and ℓ-level nodes;
  - `lem:plus-sm`(i), conditional on an explicit pair-count hypothesis;
- does not check `lem:plus-sm`(ii), the exact computations, `def:plus-schedule` as one solver,
  `thm:plus`, running time, Las Vegas behaviour or determinism;
- is not counted in the Lean table;
- is pending review.

### Adversarial self-check (Round 2)

- **Moving text.** Part C moved three blocks: the presentations paragraph, the classical proof,
  and the promoted flat-subspace section. Every label is preserved and the build has no
  undefined references.
  - Prose that says "below" or "above" across the moved blocks was not swept. One such phrase,
    the provenance reference to the paragraph's old location, was found and fixed.
  - The intro no longer contains the presentations paragraph, so a reader of the intro loses
    it.
- **The "c ≥ 10" qualifiers sit only where the brief and the referee put them, plus the
  places I found by grep.** Some other full-version sentences still say "assumes Theorem
  is-import" for results that call Theorem main. These are conservative, not false:
  `prop:tb-recursion` and the paragraph on l. 1945/1966.
- **Unchecked mathematics.** I did not re-check the IS-free mathematics. The verdict PROVED
  WITH FIXES is the referee's, and it rests on `sec:plus`, which is refereed by AI only. The
  HSP23 edits are wording and status changes, not re-derivations.
- **STRONGER rows.** Six map rows are now STRONGER than the frozen snapshot: `thm:main`, the
  four corollaries and `cor:plus-chain`. The core is consistent only once the integrator
  applies the same edits there.

## Round 3 (2026-11-14)

AI-run (Claude), pending human review. This round mirrors, into the full version, the
findings of `2026-11-14-rees-core-slim-final-referee.md`, wherever the full version has the
same text. The script is `2026-11-14-rees-full-sync/scripts/round3.py`; its anchors are
uniqueness-checked and it is not idempotent. It edited only `main.tex`. `core/` and
`numbers.tex` are untouched, and no Git commands were used.

**Result.**
- Build: 281 pages; 0 errors; 0 undefined or multiply-defined labels; 0 overfull boxes; no
  float or pdfTeX destination warnings.
- `test_rees_paper_numbers.py`: 2 passed.
- Superset map regenerated: 0 MISSING.

### Findings mirrored

**M1 (applied).** The full version's `thm:main` header says "for $c \le 9$ no assumption is
needed". So I moved the 38/53 clause out of part (4):
- part (4) now ends at "In particular $E_+(9) = 20$";
- the paragraph after the theorem states $E_H(9) = 38$ and $E_1(9) = 53$, citing their lemmas,
  and adds "both schedules use Theorem is-import".

The full version proves these values itself, so I did not add the core's "proved in the full
version" clause.

**M3.** After "So $A^+_\kappa(a)$ and $e^+_\kappa$ depend only on $(p,\kappa,a)$" I inserted
the referee's sentence, verbatim. It says:
- a chain with $\Delta_t \supsetneq$ lift changes no arity, by restriction, or by dropping a
  step whose lift is $\{0\}$;
- the computations therefore take $\Delta_t =$ lift.

This restriction argument is the referee's, and has not been refereed.

**M4.** `thm:plus-free`(ii) now asserts the strict inequality only for $\kappa \ge 2$. The
closing paragraph now reads "$2 \le \kappa \le 9$".

**M5.** Proof Overview, "Solve and compile": the halving and the contractions supply the
solutions. The Ivanyos–Santha collision step is used only for $c \ge 10$ and is never run for
$c \le 9$.

**M6.**
- **Ivanyos's scope.** The status section and `rem:main-solver` now say, in the referee's
  wording, "confirmed only the bound fix for [IS15, Theorem 3]: the exponent of a+1 printed
  there is a mistake, and its proof gives the full-depth arity $G(d,a)^{\lceil\log_2(d+1)\rceil} = \bar B_d(a)$".
  This drops the undefined $C(d,a)$ from `rem:main-solver`.
- **$C(d,a)$ defined.** It is now defined where it first appears, in `rem:is-printed`, as the
  number of variables that the proof of IS15 Theorem 3 needs for $a$ equations of degree $d$.
- **History of the $c \le 9$ result.** It now reads "applied here after that review and not
  re-refereed".

**M7.** The full version does not have the abstract sentence. Its copy in the introduction
("Fewer than $c$ evaluations do not suffice for every $H$") now reads "With fewer than $c$
evaluation points the pulled-back subgroup is not dilation-invariant for every $H$". The
full version's abstract has no such clause, and its length was not in scope.

**M8.** "in both" now reads "in all three".

**m1.1.** I renamed all 48 raw `\varepsilon` in `main.tex` to `\zeta`:
- the definition of `\eps` is left as it is;
- every renamed occurrence is the type parameter of Sections `sec:halving` and `sec:plus`,
  `thm:plus-free`, or the "Classes" paragraph;
- the error `\eps` is untouched;
- elsewhere $\zeta$ occurs only in `prop:dl-central-scalars`.

The appendices' own `\varepsilon` were left alone: those uses are local and are not this
parameter.

**m2.** Both forward references to $\mathcal H^+$ now point to "Definition plus-schedule
below".

### Self-check

- **Notation.** The ζ rename is mechanical. I grepped every raw `\varepsilon` in `main.tex`
  before renaming, and all of them were in the halving and 1H+ material (l. 987–1358 before
  the rename).
- **Remaining clash.** `lem:plus-free-const` still uses the Schedule 1H symbols `\mathcal H_D`,
  `A_D`, `K_D` (referee m1.2). It was not in this round's list, so it is unchanged.
- **Not mirrored:** M2 and m3–m10. M2 does not apply here: the full version proves the four corollaries that `cor:main-free` names.
