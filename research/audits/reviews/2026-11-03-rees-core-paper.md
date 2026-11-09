# Rees HSP core paper (campaign 4, item 7; referee F1)

Date: 2026-11-03. Author: one AI session (Claude Opus 5.5). **AI-checked, pending human
review.** No claim gate changes because of this work, and `main.tex` and the appendices
were not edited.

Output: `docs/papers/rees-hsp/core/main-core.tex`, with copies `core/references.bib`
(plus one added entry, `Olson1969`) and `core/numbers.tex` (verbatim copy of the generated
file). Build: `cd docs/papers/rees-hsp/core && latexmk -pdf main-core.tex`.

## 1. What the core paper contains

Title: "Grading a Cover: A Quantum Algorithm for the Hidden Subgroup Problem in Lazard
p-Groups of Fixed Class" (referee m8). 26 pages, 11pt, 1in margins.

| § | Content | Source in `main.tex` |
|---|---|---|
| 1 | Barrier, core idea, Def. `def:input-contract`, Thm `thm:main` (now states the explicit query count, referee M3), related work, proof overview (new), one verification-status paragraph | §1, trimmed |
| 2 | Preliminaries: BCH/Lazard facts, coset states, **Lemma `lem:fourier`** (new: Fourier sampling and the rank bound, with proof) | prose in §1, §3.2 |
| 3 | `thm:rees-cover`, `lem:homogeneous`, **`lem:lifted-source`** (new: the oracle-to-coset-state step, with proof), `prop:single-evaluation`, `lem:copy-lift`, Dixmier–Lister example | §2 |
| 4 | **`lem:instrument`** (new: phase-estimation implementation of Π_λ, with proof), `lem:central`, `prop:descent`, `rem:product-channel` (restated as a fact), recursion | §2.5, §3.1–3.2 |
| 5 | Schedule 1: `thm:is-solver` (cited), `rem:is-printed` (printed vs proved IS17 bound), **`lem:bezout`** (new proof of the reduced-degree conversion), `rem:zero-sum` (was `thm:power-sde`(iii)) | §3.3 Schedule 1 |
| 6 | `thm:uniform-compilation` with full proofs, **restricted-domain `lem:hybrid`** (replaces the body's diamond-norm hybrid and the note it cited), `cor:approx` (new) | §4.1, §3.2 |
| 7 | Proof of `thm:main`: procedure, ideal correctness, approximation with an explicit N_QFT, query count with the C_c derivation, running time; **Heisenberg example** (new) | "Proof of Theorem" paragraph, §3.2 |
| 8 | `lem:collision`, `prop:classical-query`, Table `tab:query-crossover`, `rem:query-separation` | §7.2, unchanged math |
| 9 | Outlook (prose only, no theorem environments) | see §2 below |
| App. A | Artifacts: full version, exact computations, finite checks, Lean boundary | all file paths |

## 2. What was cut and where it went

| Cut from the body | Where it is now |
|---|---|
| Status box, "previous version" passages, AI-provenance notes in theorem titles | Dropped. One paragraph, §1 "Verification Status", says the proofs were checked by AI sessions and await human review; the abstract ends with the same label. |
| Schedule 2 (`thm:power-sde`(ii)), `prop:decoupled-sde`, `rem:two-level-threshold-size`, `prop:triangular-sde`, `rem:triangular-scope`, `rem:combined-schedule` | Outlook, "Smaller arities on large fields", with status sentence. `thm:power-sde`(i) became part of `lem:bezout`; (iii) became `rem:zero-sum`. |
| Schedule 3 (`thm:random-column`, `thm:free-coordinate`, `prop:rc-lower`) | Outlook, "Using the label law". |
| `cor:fpt-r`, `cor:codim`, `rem:codim` (filiform counterexample kept in prose) | Outlook, "Derived dimension and hidden codimension". |
| `thm:ring-to-field`, `prop:black-box`, `thm:bb-envelope`, comparison remark | Outlook, "Prime-power exponent and black-box groups". States plainly that the black-box result is conditional and not claimed (referee M1, option (b)). |
| `thm:subspace-source`, `cor:subspace-hsp`, `rem:mixed-source` | Outlook, "Other symmetry sources". |
| `rem:premature` | Outlook, "Interfaces that measure early". |
| §7.1 filters (`prop:conjugation`, `rem:filters`) | Outlook, "Applications" (referee m6). |
| `prop:refresh` and its counterexample | Dropped (referee m4: unused by Thm main). |
| Finite-control, end-to-end, gate-level and single-evaluation paragraphs; resource tables `tab:full-grade-budget`, `tab:random-column-budget`, `tab:fcs-budget` | Appendix A, one bullet each (referee m5, m11). |
| §8 Lean table and guard counts | Appendix A, one paragraph on what is kernel-checked (referee m7). |
| Reproducibility section, single-evaluation negative control | Appendix A. |
| Main table `tab:main-regimes` | Dropped; its conditional rows are the Outlook paragraphs. |
| IS-solver artifact paragraph inside Schedule 1 | Appendix A. |

Every Outlook paragraph ends with "Status: …", naming the full version's appendix where one
exists. Appendix letters are not cited, because the integrator may reorder them; the
appendices are named by topic and file.

## 3. Statements whose proof was incomplete once cut out, and what I did

1. **Hybrid lemma vs. compilation (fixed; affects `main.tex` too).** `main.tex`'s
   `lem:hybrid` assumes a diamond-norm bound for each instrument "for every possible
   choice". But `thm:uniform-compilation`(iii) gives QFT accuracy only on the canonical
   subspace with clean workspace, and it bridges the gap by citing "the restricted-domain
   hybrid of the note" (`research/REES_UNIFORM_INSTRUMENT_COMPILATION.md`). Cut out of the
   repo, the proof of Thm main therefore had a missing step. The core states and proves
   `lem:hybrid` in the restricted-domain form: ideal steps preserve canonical subspaces,
   each implemented step is close only on those subspaces, and the telescoping sum compares
   each step on an ideal prefix. The paragraph after it derives the hypothesis from the
   operator-norm QFT bound. Status: proved here (argued), AI-checked.
2. **Kitaev precision with no room for synthesis (fixed; affects `main.tex`).** `main.tex`
   takes ε' = η²/(4p), which uses the whole η on Kitaev's construction and leaves nothing
   for finite-gate synthesis. The core takes ε' = η²/(16p), so Kitaev's precision is η/2,
   and it gives η/2 to Solovay–Kitaev synthesis.
3. **BCH bracket count (changed; affects `main.tex`).** `main.tex` says "exactly
   (d−1)d(d+1)(d+2)/6 bracket evaluations". That is the count of the non-memoized artifact
   `theorems/uniform_bch_rees.py`. The core derives the ODE Z' = ψ(ad_Z)Y, gives the
   coefficient recurrence, and shows that memoizing W^{(k)}_o uses at most (d−1)d(d+1)/2
   brackets (3 at d = 2, checked by hand on the class-two series). Appendix A records the
   artifact's count. This also answers referee m9 ("at most", with a derivation).
4. **Error budget (restated).** `main.tex` uses η = ε/(3 N_instr q_max), with q_max taken
   from the note's schedule. The core counts the Fourier transforms directly,
   N_QFT = (m+t)(P n + Σ_d N_d(2M_d g_d + D_{d−1}) + m) with N_d = Π_{2≤d'<d} M_{d'}, and
   takes η = ε/(3 N_QFT). This rests on `lem:instrument` (2g_d transforms per instrument)
   and on the observation that all other operations are exact reversible arithmetic. The
   two budgets agree.
5. **Steps that `main.tex` asserted in prose, now proved.** These are the oracle-to-coset-state
   step (`lem:lifted-source`), the implementation of Π_λ (`lem:instrument`), Fourier
   sampling and the rank bound (`lem:fourier`), and the Bezout reduced-degree conversion
   (`lem:bezout`).
6. **Remaining external dependencies of Thm main.** These are cited rather than proved,
   which is acceptable for a journal paper:
   - the Lazard correspondence in subgroup form [Lazard, Khukhro];
   - the Ivanyos–Santha solver: deterministic, arity B_d(a), time poly(a, log p), with the
     printed-bound caveat kept as `rem:is-printed` [IS17, van de Woestijne];
   - Kitaev's arbitrary-modulus QFT and Solovay–Kitaev synthesis;
   - von Staudt–Clausen, and the derivative of the exponential map.
7. **Statements cited but weakly sourced.** `rem:zero-sum` uses the Davenport constant of
   C_5², now cited to Olson 1969 (entry added to `core/references.bib` only; its details are
   from memory and were not checked against the journal). The Heisenberg example cites
   Chevalley–Warning to Lidl–Niederreiter, Chapter 6; that chapter number was not checked
   against the book.
8. **Dixmier–Lister non-gradability** rests on an exact computation (the row certificates),
   which is cited to the artifact. Thm main does not use it.

No statement kept in the core relies on a cut result. The Outlook makes no claims and uses
no theorem environments.

## 4. Independent check

A fresh general-purpose subagent read the whole core file as an unanchored referee. It was
not given my conclusions. It found **no error in Thm main**. It confirmed the following:

- `lem:fourier` (up to a sign), `lem:lifted-source`, `lem:instrument` and `lem:bezout`;
- the ODE and recurrence of `thm:uniform-compilation`(i). It checked them numerically against
  log(e^X e^Y) for d = 2…6, with bracket counts 3, 12, 30, 60, 105 = (d−1)d(d+1)/2. It also
  confirmed the denominators;
- the Kitaev precision choice, `lem:hybrid`, `cor:approx`, N_QFT and N_d;
- the Heisenberg example, the C_c bound (exponent 145 at c = 9) and the table's log₂ Q
  values.

Its findings, and what I did:

| Finding | Kind | Action |
|---|---|---|
| U_f is defined only on canonical encodings, but approximate QFTs can feed it non-canonical queries, so the implemented procedure was not a channel on the full space | gap | **Fixed.** Each call is now guarded by an exact canonicity flag (§6 intro). |
| Free-coordinate arity in the Outlook dropped the O(log(1/τ_d)/log(p/κ_d)) term and the hypothesis κ_d < p−1 | error (Outlook) | **Fixed.** Restated as in `thm:free-coordinate`(iii). |
| Outlook status for Schedule 2 said "proved"; `main.tex` says part (ii) is conditional. The triangular variant lacked p ∉ E₂(κ); codim status; ring-to-field had no status; subspace said "proposed, conditional", r supplied | wording | **Fixed.** All aligned with `main.tex`. |
| Sign in `lem:fourier` (FR_hF† has ω^{−h·y}) | wording | **Fixed.** Harmless, since J = −J. |
| B_d was defined only for d ≥ 2, but used at κ = 1 | wording | **Fixed.** Now d ≥ 1, so B_1(a) = a+1. |
| `thm:uniform-compilation`(i)–(ii) was stated for G_d, but the copy-lift needs G = (L, ∗) | wording | **Fixed.** Now stated for any algebra of class ≤ d. |
| "class c and exponent p" were attributed to Thm `rees-cover`(iii) | wording | **Fixed.** Now cited to Khukhro Ch. 9–10. |
| Class-9 profile was written (17,16,…,1) | wording | **Fixed.** Now (17,16,14,12,9,6,3,1). |
| "For higher class two related obstacles" | wording | **Fixed** with a comma. |
| B_d is an intermediate step of the IS17 proof, not its printed theorem; no page cited | citation | **Left.** `rem:is-printed` names Thm 11 and §3.3 of arXiv:1503.09016v2; the page was not checked. |
| Kitaev 1995 is a preprint, and its precision formula 2(qε')^{1/2} was not rechecked here | citation | **Left.** Cleve–Watrous §7.1 is cited as an alternative. A refereed arbitrary-modulus QFT citation would be better; see "Missing". |
| Derivative of exp and von Staudt–Clausen are uncited | wording | **Left.** Both are textbook facts. |


## 4b. Follow-up: the round-4 core check (`2026-11-03-rees-check-core.md`)

I checked the core file against that report's gaps G1 and G2 and its minor items.

- **G1 (hypothesis mismatch between `lem:hybrid` and `thm:uniform-compilation`(iii)).** The
  core already closed this. Its `lem:hybrid` takes the restricted-domain hypothesis: canonical
  subspaces preserved by ideal steps, and closeness only on states supported there. The
  telescoping proof applies each difference only to ideal prefixes. The paragraph after the
  lemma derives the hypothesis from the operator-norm QFT bound, so the core never uses the
  diamond-norm form, and the report's QFT_3 ⊕ (±1) example does not apply to it. One step was
  implicit: the report's P1 asks that the state set be closed under conditioning on classical
  values. **Changed:** S_j is now defined as the span of computational basis states, classical
  records included, with canonical encodings and clean workspace. A sentence notes that
  conditioning on a classical value keeps support in S_j. The guarded oracle call (§4 above)
  makes every implemented step a channel on the full space.
- **G2 (N_instr undefined; "complete instrument" used in two senses).** The core does not use
  N_instr. It counts the Fourier transforms directly, as N_QFT. This count is the report's
  N_instr = S(P + Σ_d Π_{d'<d} M_{d'} + 1), weighted per node by n, 2M_d g_d + D_{d−1} or m.
  It allots η = ε/(3N_QFT) per transform. "Complete central instrument" means only the single
  central measurement of `lem:instrument`. **Changed:** one sentence in the proof of Thm main
  now says that N_QFT is fixed before the run, because the Schedule 1 arities are public and
  fixed and there are no restarts.
- **Minor m1 (λ is both the dilation scalar and the central label).** **Changed:** the
  dilation scalar is now θ throughout §§1–3 (δ_θ). λ is kept for labels, and the
  Dixmier–Lister parameter λ is local to its display.
- **Simulation count.** **Changed:** Appendix A now says the end-to-end simulation's 32
  subgroups are 23 instances with default options plus 9 with its F_7 option, which the check
  did not run.
- The report's P1–P3 target `main.tex` and are left to the integrator. The core's versions
  match them in substance.

Build after these changes: from a clean copy of the three source files in the session
scratchpad. Exit 0, no warnings, no overfull or underfull boxes, no undefined or missing
references, 26 pages, no `??` in the extracted text. `docs/papers/rees-hsp/core/` now holds
only `main-core.tex`, `references.bib` and `numbers.tex`.

## 4c. Follow-up: second referee (`2026-11-03-rees-referee-2.md`)

Applied to `core/main-core.tex`, mirroring `main.tex` I125–I126:

- **P1 / F1, F3, F4 (`thm:main`).** The theorem is now self-contained. It assumes
  `thm:is-import`, uses γ_{c+1}(L) = 0, and lists inputs (a) oracle and (b) fresh independent
  copies, with H arbitrary. It names the points 1, …, c and Schedule 1 with M_d = B_d(g_d).
  It outputs a basis of log H and hence generators of H. It keeps the query/copy count Q_q
  with its C_c bound, the poly_c gate bound, and the clause "no property of H is assumed".
  The sentence after the theorem names the three imported ingredients and notes that c may be
  any upper bound on the class below p.
- **P2 / F2, §1.9 (`thm:is-import`).** This replaces the core's former `thm:is-solver`, which
  had omitted the hypothesis d | p−1. It is the cited theorem in the form used: deterministic,
  d | p−1, M ≥ B_d(a), time poly(M, log p), and explicit output s_i. The new `rem:is-import`
  covers five points:
  - (a) the s_i themselves are returned, which `prop:descent` needs;
  - (b) d ∤ p−1 is handled by `lem:bezout`;
  - (c) points to `rem:is-printed`;
  - (d) determinism is not essential, since Schedule 1 leaves a third of the budget unused;
  - (e) the reading was AI-checked only.

  Schedule 1 is now a named paragraph. It runs `thm:is-import` at degree κ_d on the first
  B_{κ_d}(g_d) of the B_d(g_d) columns, gives the rest weight 0, and lifts by Bezout. The
  proof of Thm main cites this path. `lem:bezout` now states its conclusion through
  `thm:is-import`.
- **§1.7 (minor).** The hybrid paragraph now says that S_j is the tensor product of the local
  canonical subspaces, so the rest of the system is the reference for each local QFT bound.
- **P3 / 2.0 (status convention).** One sentence was added to the verification paragraph:
  proved statements are unqualified, imports are cited theorems named in hypotheses, and
  computer searches are marked. The core's theorem headers already carry no status tags.
- **§3.3 (undefined terms).** A "Terminology" paragraph after `lem:copy-lift` defines
  source, lifted source, merge, terminal sample and label width. The core never uses
  "receiver", and §2.7's per-instrument transform count was already explicit (N_QFT).

Checked and not applicable, or left:

- §2.1 (the Appendix B hybrid), 2.4, 2.5 and P4–P11 concern appendices or results that the
  core cut to the Outlook.
- §2.2 (triangular solver "deterministic"): the Outlook does not claim determinism.
- §2.3 (premature measurement, mixed source): the Outlook labels both as argued and not
  claimed.
- §2.6 (E_2(7) inconsistency between `main.tex` and appendix-schedule2): the Outlook follows
  `main.tex` ("computed exactly for κ ≤ 7"). The inconsistency is the integrator's to resolve.
- §3.1 / P7 (cite an archived snapshot by commit hash): not possible while the work is
  uncommitted. Appendix A should gain the hash once the work is committed.

Build: from a clean scratchpad copy of the three sources. Exit 0, no warnings, no
overfull or underfull boxes, no undefined or missing references, 26 pages, no `??`. `core/`
holds only the sources.

## 5. Build log summary

`latexmk -pdf -interaction=nonstopmode main-core.tex` (pdfTeX, BibTeX `plain`). Exit 0.
The final log has no LaTeX or package warnings, no undefined references or citations, no
"referenced but does not exist", no multiply-defined labels, and no overfull or underfull
boxes. Two underfull boxes in the bibliography were removed by setting it ragged-right.
The final build is from scratch (`latexmk -C`, then a build). Output: `main-core.pdf`,
**26 pages**. A text extraction of the PDF has no `??`. Later builds run in a scratchpad copy; the repo folder holds only the sources.

## 6. Exact statement that now holds; what is missing; claim gates

- **Holds (AI-checked, pending human review):** the core file is a self-contained proof of
  Thm main. Assume the explicit Lazard chart with p > c, fixed c, and oracle or coset-copy
  input. Then the procedure returns a basis of log H with probability ≥ 1−ε, using
  c(m+t)Π_d B_d(g_d) queries with t = ⌈log_p(3/ε)⌉. Its running time, gate synthesis
  included, is polynomial in m, log p, w and log(1/ε). It depends only on the published
  sources listed in §3, item 6. The classical bound Θ(p^{(m−1)/2}) is proved in full.
- **Missing:** human review. A refereed citation for the arbitrary-modulus QFT precision
  bound (Kitaev 1995 is a preprint). A page reference for the IS17 intermediate bound. The
  page count is 26, in the lower part of the target. The core
  repeats `main.tex` text, so later edits to `main.tex` will not propagate; `core/numbers.tex`
  is a copy that `make_numbers.py --check` does not check.
- **Claim gates that must stay false:** none changed. The black-box result, Schedules 2 and
  3, fpt-r, codimension, torsion and subspace results remain conditional, and the core
  states each as not claimed.

## Proposed paper text (notes for the integrator)

These are fixes the core makes that `main.tex` lacks. Target: `main.tex`. Status:
AI-checked, pending human review. The exact LaTeX is in `core/main-core.tex` under the
labels given.

1. Replace `lem:hybrid` and its proof with the restricted-domain version
   (`core/main-core.tex`, Lemma `lem:hybrid` and the paragraph after it). Then drop "By the
   restricted-domain hybrid of the note" from `thm:uniform-compilation`(iii).
2. In `thm:uniform-compilation`(iii), replace "Kitaev's precision 2(pε')^{1/2} is met with
   ε' = η²/(4p)" with the core's sentence: ε' = η²/(16p), precision η/2, and η/2 for
   synthesis.
3. In `thm:uniform-compilation`(i), replace "exactly (d−1)d(d+1)(d+2)/6" with "at most
   (d−1)d(d+1)/2 (memoized; the artifact's unmemoized recurrence uses
   (d−1)d(d+1)(d+2)/6)", using the core's proof of (i). The gate-level paragraph's "the bound
   in (i) gives 48" would then read 36 (12 passes × 3).
4. Optionally adopt `lem:fourier`, `lem:lifted-source`, `lem:instrument` and `lem:bezout`
   as stated lemmas in place of the corresponding prose.
5. Add the oracle canonicity guard (core §6, first paragraph) to `main.tex` §4. `main.tex`
   has the same gap: its hybrid needs every implemented step to be a channel on the full
   register space, but U_f is specified only on canonical encodings.
