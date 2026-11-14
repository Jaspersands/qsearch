# Slim draft of the Rees core paper (helper report, 14 November 2026)

All of this is AI-checked and pending human review.

## Verdict

> **Round 2 (below) supersedes this verdict.** The draft is now 43 pp., the Schedule 1 proofs are restored, and Theorem main again depends on no proof outside the core.

`research/audits/reviews/2026-11-14-rees-core-slim/main-core-slim.tex` compiles cleanly:
- nice -n 19 pdflatex, bibtex, pdflatex, pdflatex;
- 0 undefined references, 0 errors, 0 overfull boxes and 0 BibTeX warnings (10 underfull boxes);
- **44 pages** in all, against 68 before. The main text runs from p. 1 to p. 40 (≈ 39 pp.), Appendix A is pp. 40-42 and the references are pp. 42-44.

The 40-page total and the ≲ 32-page main-text target were **not** reached. Section 5 (Schedules 1, 1H and 1H+) is 16 pages on its own, and the brief requires the 1H and 1H+ statements and proofs to stay. Theorem main still has all its parts and the exponents 20, 38 and 53. I added no new mathematics and, as far as I can tell, strengthened no claim (see the self-check).

## Files

- `2026-11-14-rees-core-slim/main-core-slim.tex` and `.pdf` are the draft. Never edit the `.tex` by hand: it is generated.
- `2026-11-14-rees-core-slim/build/template.tex` is the source of the draft. `build/assemble.py` pulls verbatim line ranges (`@@L a-b`) from `orig-main-core.tex`, and `build/make.sh` builds.
- `2026-11-14-rees-core-slim/cut_manifest.md` has 68 rows, one per removed or condensed item, with line numbers in the snapshot `2026-11-14-rees-full-sync/core-snapshot-68pp.tex`. The snapshot is byte-identical to the 68-page core.
- `orig-main-core.tex`, `numbers.tex` and `references.bib` are copies. `docs/papers/rees-hsp/core/main-core.tex` is unchanged: md5 `71743611d8b66af3e0d485110953a9e1`, the same before and after.

## Structure before and after (pages)

| Part | 68-pp core | Slim |
|---|---|---|
| 1 Introduction | 2-13 (≈12; Related Work 9-12) | 2-9 (≈7.5; Related Work 6-8) |
| 2 Preliminaries | 14 (1) | 9-10 (1) |
| 3 Rees cover, tuple oracle, non-gradable example | 15-19 (≈4.5) | 10-13 (≈3) |
| 4 Measured central descent | 19-21 (≈2.5) | 13-16 (≈2.5) |
| 5 Schedules 1 / 1H / 1H+ | 21-40 (19: 5 / 4 / 10) | 16-32 (16: 3 / 4 / 9) |
| 6 Uniform compilation, error composition | 40-42 (2) | 32-35 (2.5) |
| 7 Proof of main theorem and examples | 42-46 (4; Heisenberg and class three) | 35-38 (3; class three plus rem:black-box) |
| 8 Black-box, presentations, UT_n(Z) | 46-55 (9) | none (one remark, rem:black-box, in Sec 7.1) |
| Classical query complexity | 55-58 (3, as Sec 9) | 38-39 (1.3, as Sec 8) |
| Outlook | 58-59 (1) | 39-40 (1) |
| App A Artifacts | 59-64 (5) | 40-42 (2, table) |
| App B Classical proof | 64-65 (1) | none (full version) |
| References | 65-68 | 42-44 |

The page ranges overlap at section boundaries, so the counts are approximate.

## Judgement calls

1. **Background (old Sec 1.1) folded.** It became one opening paragraph (Lazard correspondence, gradings) and a Heisenberg "Example." paragraph in Core Idea. That paragraph stands in for the deleted Heisenberg example subsection. The kept worked example is the class-three one (Sec 7.1), condensed, because Remark free23 and Section 3 refer to it.
2. **Schedule 1 lemma proofs sketched.** I read the brief's "Schedule 1 interface (statement plus what is imported)" as allowing the proofs of lem:zero-sum-length (Chevalley–Warning, Weil, small-p search) and lem:exponent (Dirichlet lower bound, 2-adic case analysis giving 53) to move. Both now have a "Proof sketch; the full proof is in the full version". This changes the core's self-containedness: see Finding 2. If the integrator disagrees, restoring S 596-605 and 638-650 costs about 1.5 pages.
3. **Kept in full:**
   - Sections 3-4, Lemma rounds, Lemma bezout;
   - Schedule 1H: lemmas stage, finish and two-term, Def schedule1h, Thm halving (i) and (iii) with proofs, and Lemma halved-exponent;
   - Schedule 1H+: all lemmas, Prop plus-tables, the thresholds table, Thm plus, Lemma plus-exponent and Remark plus-is;
   - Theorem uniform-compilation (i)-(iii), the hybrid error argument and the proof of Theorem main.

   Only the cost-recursion parts (ii) of Thms halving and plus were condensed to induction sketches. The per-prime lists in Lemma plus-exponent became counts.
4. **Section 8 replaced by rem:black-box** (statements (i)-(iv), each marked "proved in the full version", with their conditions). As a result:
   - the abstract's corollary sentence now says "Corollaries in the full version";
   - the black-box items in "What is new", the Outlook and Open problem (4) were redirected.
5. **The tocdepth was set to 1** to shorten the table of contents.
6. **Caveats.** Each is stated once in Sec 1.6, in three paragraphs: "The import", "The exponents" and "Results of the full version". The repeats in rem:main-solver, rem:is-printed, the 1H+ introduction and the Outlook now refer back to Sec 1.6.

## Statements whose wording changed (old → new)

Theorem and lemma statements are verbatim, apart from the abstract and the remarks below.

- **Abstract.** "Corollaries give the same guarantee for black-box p-groups ..." → "Corollaries in the full version give the same guarantee for black-box p-groups ...".
- **Title footnote.** "Core version." → "Core version; the full version is the ancillary file anc/rees-hsp-full.pdf."
- **Dependency on the full version.**
  - Old App A: "Nothing claimed in this paper depends on it; every proof of a claimed result is given here".
  - New Sec 1.6: "Theorem main depends on the full version only for the details of the proofs of Lemmas zero-sum-length and exponent, which are sketched here."
- **rem:main-solver, ending.** The list beginning "The exponent 20 at c = 9 rests on Lemma rounds ..." and ending "... refereed by AI only, pending human review" → "The results on which the exponents 20, 38 and 53 rest, and what G. Ivanyos's confirmation covers, are listed in Section status." Sec 1.6 now carries the same content.
- **Status, the exponents.** The nested "rests on everything 53 rests on and, in addition" chain became "rests, in addition, on ..." with the same items and verdicts. One item was **kept verbatim even though it may be stale**: "The write-up of Section plus, which merges the two drafts, has not itself been refereed" (Finding 3).
- **Obstacle (1).**
  - Old: "If the Lazard Lie algebra L of a p-group of class c<p is positively graded, ... then δ_θ(x_k) = θ^k x_k defines automorphisms. The top nonzero component L_D is central and δ_θ scales its characters by θ^D."
  - New: "The top component L_D of a positive grading is central, its dilations scale its characters by θ^D, and such scalings ...". Gradings and dilations are now defined in the opening paragraph.
- **Dixmier–Lister.**
  - Old: "Solving it over Q gives the family of derivations [two displays] with λ, μ, ν, ρ and x_1, ..., x_4 ∈ Span(e_7, e_8) free; the coefficient matrix has rank 52 = 64−12 ..."
  - New: "Over Q the derivations of L_DL form a 12-dimensional space (and the coefficient matrix of the derivation equations has rank 52 = 64−12 modulo every prime 5 ≤ p ≤ 23; exact computation)". The dimension 12 = 4 + 8 is the old parameter count. An earlier draft of mine dropped "Over Q" and the rank qualifier; I caught and fixed that.
- **rem:is-printed.**
  - Old: "Reading log as log_2 (or as ln or log_10), the second inequality fails for every d ≥ 2 once a is large ... Only the first inequality is established by the proof."
  - New: "For any of the usual bases the second inequality fails for every d ≥ 2 once a is large, because d⌈log_2(d+1)⌉ > d log_2 d."
  - The old sentence listing what the confirmation does not cover now reads "What the confirmation covers is stated in Section status". Sec 1.6 repeats its whole content.
- **rem:query-separation (a), restored sentence.** "Theorem main adds polynomial running time at polynomially many queries; it does not lower the query count, and its count is far above the information-theoretic one." Finding 1 explains why it is restored.
- **rem:query-separation (b).**
  - Old: "Below the crossover primes of Table query-crossover, the stated quantum bound gives no query advantage."
  - New: "Below explicit crossover primes, tabulated in the full version (at δ = ε = 1/3, for example p = 29 for the Heisenberg group and p = 61 for the free two-generator class-three group), the lower bound of Proposition classical-query(i) does not exceed the stated quantum bound, so the stated bound gives no query advantage there."
  - The new wording follows the old table caption: the crossover is "the smallest prime p at which the bound ... forces more than Q_q classical queries".
- **Outlook status.**
  - Old: "the Schedule 2 and triangular arities, the exponents 2c−1 in the stated ranges and the values 143, 40 and 99 are AI-checked and refereed by AI, pending human review; the block-steered variant, Schedule 3 and the value 37 remain conditional".
  - New: "the Schedule 2 and triangular arities and the exponent 2c−1 in the stated range are refereed by AI; the block-steered variants and Schedule 3 remain conditional". The section's first sentence says all items are AI-checked and pending human review, and the values 143, 40, 99 and 37 are no longer quoted.
- **Small re-pointings and moves:**
  - Prelim: "(Corollary black-box-pe)" → "(used only in the full version)".
  - rem:free23: "proved in the research notes listed in Appendix A" → "proved in research notes, listed in the full version (Appendix A)".
  - The 1H+ introduction's status sentence → "stated in Section status; in particular the merged write-up has not itself been refereed".
  - Example 7.1: "Lemma plus-exponent(ii) below" → "below that". The old phrase meant a range of primes, not a forward reference.
  - The rem:proof-uses sentence "Lemma central is needed only for the exactness of ρ_λ, not for the uniformity of λ" was moved into the paragraph opening Schedule 1.
- **Lean paragraph.** Condensed. Every stated limitation is kept: the c = 3..7 discharge (c = 7 only with p ≥ 11), the conditional records with computational checks for κ ≤ 7, the full not-formalized list, and "no formally checked compiler".

## Findings for the integrator

1. **A sentence hidden in a comment in the 68-page core.** Line 1346 of main-core.tex is a `% NEEDS HUMAN VERIFICATION ...` comment. Its tail, "Theorem main adds polynomial running time at polynomially many queries; it does not lower the query count, and its count is far above the information-theoretic one (Table query-crossover).", is therefore not printed in the current PDF. It reads like intended text. The slim draft prints it (template line 204). The integrator should decide for main-core.tex as well.
2. **The core is no longer self-contained for Theorem main.** The slim draft only sketches lem:zero-sum-length and lem:exponent. Sec 1.6 says so explicitly, but this reverses the old App A claim that every proof is given here. If self-containedness is preferred, restore the two proofs (about 1.5 pp.).
3. **Stale verification status, not fixed (no new mathematics).** `2026-11-14-rees-core-plus-referee.md` referees the merged 1H+ write-up: CORRECT WITH FIXES, with F2 (repeated moduli), F3 (U_m gap list false per m) and F4 (the "9 < p" range for c ≤ 8). The core, and so the slim draft, still says the merged write-up "has not itself been refereed". The slim text carries Section 5.2 verbatim, so whatever is applied to main-core.tex must be applied to the slim template too.
4. **Page target.** The total is 44 pp., with about 39 in the main text. Two further cuts would each break a "must keep" rule: moving Thms halving and plus with their proofs (≈ 8 pp.), or the 1H+ lemma proofs. I did not make them.

## Honesty labels

- Theorem main and Theorem is-import: unchanged statements. PROVED given cited theorems, AI-checked and pending human review, as in the 68-page core.
- The black-box corollaries and Cor utz are not proved in the slim draft. The draft labels them "proved in the full version"; this helper did not re-check them.
- My own work is editorial only. It is a reorganization of PROVED material, not a proof, and the PDF was spot-read, not refereed.

## Adversarial self-check

- **Did a hypothesis disappear from a stated result?** I checked:
  - Theorem main, is-import, rounds, bezout, zero-sum-length, exponent, halving, plus, halved-exponent, plus-exponent and classical-query are verbatim, apart from parts (ii) of halving and plus;
  - those two parts were condensed in their proofs, not in their statements;
  - the statement of rem:free23 keeps every hypothesis ([IS15, Cor 8] with its sketch caveat, Rabin, exact QFT, p ≥ 5) and both failure cases.

  None disappeared.
- **Did a caveat that limits a claim disappear?** Compared line by line, word diffs in `build/`:
  - Two caveats had been dropped and are restored: "the numbering of the journal version ... was not checked", and the Lean limits "c = 7 needs p ≥ 11", "computational checks for κ ≤ 7" and the full not-formalized list.
  - Removed without a replacement, and judged non-limiting, or belonging only to moved results:
    - the Imran–Ivanyos v1 numbering note (Cor nilpotent moved);
    - "nilpotence and the class bound are promises and are not tested" (rem:nilpotent-scope (c); also moved);
    - "In this model a query lower bound also bounds classical running time from below" (a remark, not a caveat);
    - "the exact simulations can only falsify" (free23 notes; the remark itself says it is not relied on).
- **Did any wording strengthen a claim?** Three edits were candidates:
  - "derivations form a 12-dimensional space", fixed by restoring "Over Q" and the rank qualifier;
  - "free23 proved in the full version", reverted to research notes;
  - the Status sentence that the core does not depend on the full version, rewritten after the proofs were sketched.

  The new (b) wording of rem:query-separation restates the definition in the table caption. Finding 1 adds a printed sentence. It is a weakening statement ("does not lower the query count"), but it is still new to the printed text.
- **Is a proof step now missing from a must-keep proof?** The 1H and 1H+ correctness proofs are verbatim. The condensed parts (ii) concern expected-time recursions; the brief's "cost-recursion bookkeeping" may move. The proof of Theorem main cites uniform-compilation (iii) and corollary approx, both kept. Part (iv) of uniform-compilation (memory) is not cited by the kept text: grep finds no "(iv)" reference to it.
- **Residual risk.** I read the PDF, not every formula, so a condensed sentence may still have lost a qualifier I did not notice. The manifest's word diffs let a reviewer re-check each row.


---

## Round 2: referee fixes, the Lean addendum and further cuts (14 November 2026)

**Inputs:**
- `2026-11-14-rees-core-slim-referee.md` (ACCEPT WITH FIXES);
- the integrator's notes;
- `2026-11-14-rees-lean-schedule1hplus.md`, findings 1-3.

The template was backed up before each pass (`build/template.v7-integrator.tex` to `v11-post-pass8.tex`). The passes are `build/pass6.py` to `pass9.py`, with the helper `build/tlib.py`.

**Build.** nice -n 19 pdflatex, bibtex, pdflatex ×2: 0 undefined, 0 errors, 0 overfull boxes.
- **Pages:** 44 before this round, 43 after, of which main text 1-39, Appendix A 39-41, references 41-43.
- **The steps in between:**
  - 44 after the fixes F1-F13;
  - 45 after the Lean fixes, the artifact rows and the Lean sentence;
  - 43 after the cuts;
  - 43 after the pointer titles.
- **Section starts:**
  - Sec 1 at p. 1 (Related 6, Status 7), Sec 2 at 8, Sec 3 at 9, Sec 4 at 12;
  - **Sec 5 at 14-32** (5.1 at 18, 5.2 at 23);
  - Sec 6 at 32, Sec 7 at 34 (7.1 at 36), Sec 8 at 37, Sec 9 at 39;
  - App A at 39, references at 41.

### Fixes, and where each was applied

| Fix | Applied where | Note |
|---|---|---|
| F1 | S 733 and S 969 restored **whole and verbatim** (the full items (ii) of Thms halving and plus, a superset of the "Explicitly, ..." passages). The proof of lem:zero-sum-length (S 596-605) and **also** that of lem:exponent (S 638-650) are restored verbatim | With both proofs restored, the Sec 1.6 sentence reads: "Theorem main does not depend on the full version: every proof it uses is given here." This is stronger than the referee's first option, which kept the Lemma exponent proof as a sketch. "The exponents" no longer says "whose proofs this core only sketches" |
| F2 | Not a text fix (integrator gate). The pointers now name full-version material by title, not by number: ``The exponent of Schedule 1H+'' (proof), ``The grades at the maximizers'', ``Proof of the Classical Query Bounds'', the table of query counts in ``Classical Query Complexity'', ``Central scalars of L_DL'', ``A Non-Gradable Example'', ``Black-Box Groups and Other Presentations'', ``A cover-free algorithm for the free class-three group'', ``Direct twists beyond class two'', and Related Work | The titles are those of S. They are valid in the full version only if it keeps them (F2 grep still to run) |
| F3 | rem:query-separation (a): the referee's sentence, verbatim | |
| F4 | Sec 7.1 "Automorphisms": the F_5 sentence, verbatim. New Appendix A row "Class-three example": `R/2026-11-09-rees-paper-pass-prep/class3-example/verify_free.py` and `.out` (check [F5j] there) | The artifact was located by me; the referee did not name it |
| F5 | Kept the integrator's wording, made precise: "(verdict: correct with fixes, applied here after that review and not re-refereed)". The 1H+ intro sentence, as edited by the integrator, no longer mentions refereeing. Stale comments S 775-781 removed | The same change is needed in main-core.tex S 257, 787 and 776-781 (integrator) |
| F6 | S 976, verbatim referee wording | |
| F7 | `\fullv` → "the full version (ancillary file anc/rees-hsp-full.pdf)" | |
| F8 | Sec 1.6 "The import": referee wording, verbatim | |
| F9 | Prop dl-central-scalars and Prop classical-query titles: "; proof in the full version" | dl-central-scalars no longer says "AI-checked, pending human review" in its title. Sec 1.6 covers this globally |
| F10 | rem:black-box (ii), (iii) and (iv): referee wording, verbatim | |
| F11 | rem:is-import (c): "and van de Woestijne's zero sum" | |
| F12 | Related Work: "; the bounds of those papers are not implied by ours" | |
| F13 | S 1346 comment truncated after "IPL version not checked." | The `ARXIV-TODO` commit hash (`80256fcb`) is left as is. It is inherited and flagged for submission |
| Lean 1 | "Classes" paragraph: "For i ∈ Z_D, ξ^i means ξ raised to the representative of i in {0,…,D−1}; the preprocessing and the run use the same representatives." The "Multi-level contractions" clause is reduced to "Write z_m = ξ^m for m ∈ Z_κ" | A convention fix. Correctness does not depend on it (Lean report) |
| Lean 2 | Appendix A: the certificate, table, threshold and E_+ rows now name each file's folder explicitly (`2026-11-13-rees-headline-below-38/`, `-21-referee/`, `-21-recompute/`, `-20-referee/`, `2026-11-14-rees-schedule1hplus-draft/`), each checked with `ls` | My round-1 table wrongly put the certificate files in the draft folder; it is now corrected |
| Lean 3 | cor:plus-chain: "Δ_t = lift_{D_t}(Ω_{t-1})" → "Δ_t ⊇ lift_{D_t}(Ω_{t-1})" | **Statement change (a weaker hypothesis).** The proof is "Induction on L with Lemma plus-refine", and plus-refine's hypothesis is Δ ⊇ lift (S 809). So the proof visibly uses only ⊇; the Lean report confirms it (finding 2). The arity and constant formulas use |Δ_t| and are unchanged |
| Lean sentence | Lean paragraph: Formal.Schedule1HPlus formalizes the correctness of refinement chains, the two-class stage and finish, and tensor and ℓ-level nodes, and lem:plus-sm(i) conditionally on a pair-count hypothesis. It models no running time and is AI-checked, review pending. The "not formalized" list now names the rest of Sec 5.2: plus-sm(ii), the thresholds, prop:plus-tables, def:plus-schedule as one solver, and thm:plus | |

### Further cuts (referee table)

| Referee # | Done? | What |
|---|---|---|
| 1 | yes | Table of contents removed |
| 2 | yes | rem:free23 moved to the full version. One sentence remains in obstacle (2) (conditional on cited theorems including [IS15, Cor 8], not reviewed by a human, not used here); Related Work says "but see obstacle (2) above" |
| 3 | partly | FIMSS sentence removed; Morales and Holt–Subramanian reduced to one sentence. The scope-only, "not implied" (F12), dated-search and "cover not claimed necessary" caveats are kept |
| 4 | partly | The F_3 example after Prop single-evaluation removed. **Not merged into rem:fewer-points:** the proposition is a statement of the paper's own (for a single θ ≠ 1), stronger than the remark's k = 1 case (all θ), so merging would drop a result |
| 5 | **no** | It rewrites statement (i) of Theorem uniform-compilation (the explicit bracket counts) and replaces its proof by a new argument. That is a statement change and new text, not a cut |
| 6 | yes | Sec 7.1 stages condensed to "Stages and count" |
| 7 | **no** | Deleting rem:black-box would drop the promise and oracle conditions that F10 just added. The intro paragraph does not carry them, so the cut would undo F10 |
| 8 / 8′ | **no** | The owner's brief keeps "the classical query-complexity statement". Dropping parts (iii)-(iv), or the whole section, conflicts with it. The Nayak line was already removed in round 1 |
| 9 | partly | "Further items" merged into the paragraph "Extensions", with all status labels kept. The 95 paragraph and the open problems are kept (they carry the confirmation and conditional labels) |
| 10 | **no** | The paragraph after Thm main is the only place listing the standard imports (Chevalley–Warning, Weil, Rabin, Dirichlet, Lazard subgroup form, Kitaev and Solovay–Kitaev, Bennett). Sec 1.6 and rem:main-solver do not carry that list |
| 11 | **no** | A longtable row (0.71 text width) would lengthen the Lean paragraph, not shorten it |

### Wording changes in round 2 not quoted above

- **Obstacle (2).**
  - Old: "for this one group, Remark free23 describes a cover-free algorithm, not yet reviewed by a human, that uses no automorphism preserving H."
  - New: "for this one group, the full version describes a cover-free algorithm (remark ``…''), conditional on cited theorems including [IS15, Corollary 8], not reviewed by a human and not used here, that applies no automorphism preserving H."
- **Sec 7.1.** The new "Stages and count" paragraph keeps:
  - 15 and 16 columns (p ≡ 1 mod 3), with the availability qualifier (Lemma plus-sm for p ≥ 430, exact computation below);
  - A_3(2) = 729;
  - the counts 2^12.08 / 2^17.68 / 2^23.68.

  It drops "with equality for p > 2·10^6", the p ≡ 2 (mod 3) arities and the simulator sentence. The simulator is still in the finite-checks row.
- **Outlook status** now also lists "the codimension and stabilizer sources" as conditional, as the old "Further items" paragraph labelled them.

### Prepared, not applied: cuts once "Theorem main holds at c ≤ 9 without thm:is-import" is accepted

The slim line numbers below are those of `main-core-slim.tex` as of this round. For c ≥ 10 these must stay:
- thm:is-import (468) and Lemma rounds (490);
- rem:is-import (a), (b), (d) and (e) (476);
- Lemma zero-sum-length;
- the Schedule 1 paragraph (541).

At odd κ ≥ 11, candidate (a) is the only one.

The candidates for moving to the full version (~2 pp. by the referee's estimate):
1. rem:is-printed (485) and the B̄_d links that serve only it: B̄_d in (eq:Bd) near 150, if no other text uses it, and rem:query-separation (1044), which would be restated with B_d.
2. Lemma exponent (ii) (the values E_1(c) and 53, 544 ff.) with the (ii) part of its proof. Part (i), with c(c+1)/2 ≤ E_1(c), is kept.
3. The "53" clauses:
   - Theorem main (4) (153 ff.);
   - the paragraph after it (186);
   - rem:main-solver (182);
   - Sec 1.6 "The exponents" (215);
   - the Appendix A row for t_{p,κ} and E_1.
4. Lemma halved-exponent (i)-(ii) (the 38, 659 ff.), keeping the c_κ definition of (iii), which Lemma plus-exponent (iii) uses. Also the 1H grade-profile paragraph (677), the "38" clauses at the places listed in item 3, and the Schedule 1H row of Appendix A.
5. The Outlook paragraph "Halving at the confirmed depth" (the 95, 1062) and the `pub_hcd.py` reference.
6. Sec 1.6 "The import" and "The exponents" shrink to the c ≥ 10 caveat, rem:main-solver's ending to one clause, and rem:plus-is (902) to "superseded by" the new theorem.
7. The abstract's "with the collision step … as an imported theorem" becomes "unconditionally for c ≤ 9 and, for c ≥ 10, with the collision step … imported". This is a statement change, for the integrator.

**Caveats:**
- Lemma plus-exponent's first sentence and the last sentence of its (ii) ("switched off … values of Lemma halved-exponent(ii)") would need rewiring.
- Items 2-4 remove the 53 and 38 that the owner's round-1 brief required to stay in Theorem main. That is the owner's or integrator's decision.

### Adversarial self-check (round 2)

- **Statements changed this round:**
  - cor:plus-chain, from = to ⊇: a weaker hypothesis, so a stronger corollary. Its support is the proof's single use of plus-refine (stated with ⊇) and the Lean report. Requested by the integrator.
  - The titles of two propositions.
  - The new representative convention, which fixes objects and does not change truth.

  Nothing else in a theorem, lemma, proposition or definition changed. All restorations are verbatim.
- **F3 replacement.** The quantifier "of degree up to E_+(c)" restates Theorem main (4), and "does not depend on p once p ≥ 3/ε" restates rem:query-separation. The sentence makes no new claim.
- **F4 artifact.** Line [F5j] of `verify_free.out` reads "so Stab(h) acts on the centre by every cube scalar, for EVERY subgroup". It is a finite check at p = 5, consistent with "(exact computation)".
- **The Lean sentence** paraphrases the verdict section of the Lean report. That report says that `prop:plus-tables` and the ℓ-level tables are not checked in Lean. The draft says they are not formalized, and does not claim the ℓ-level formalization is non-vacuous for the tables.
- **Dropped this round:**
  - from Sec 7.1: "with equality for p > 2·10^6" (an illustrative sharpness remark);
  - from Related Work: the FIMSS scope sentence.

  Neither is a caveat limiting a claim.
- **Not verified:** that the full version uses the titles I point to (F2); the plus-referee fixes themselves; the PDF beyond the build counts and grep checks (no full re-read of the 43 pages).

---

## Round 3: Theorem main without the import for c ≤ 9, and the IS-dependent cuts

**Inputs:**
- `2026-11-14-rees-is-free.md`, `2026-11-14-rees-is-free/fragment.tex` and `edits.py`;
- `2026-11-14-rees-is-free-referee.md` (PROVED WITH FIXES).

**Passes:** `build/pass10.py` (integration), `pass11.py` (cuts, acknowledgment pointer) and `pass12.py` (wording). Backups: `template.v12-round2-final.tex`, `v13-post-pass10.tex` and `v14-post-pass11.tex`.

**Build.** 0 undefined, 0 errors, 0 overfull boxes.
- **Pages:** 43 (end of round 2) → 46 after the integration → **45** after the cuts. Main text is pp. 1-41, Appendix A 41-43, references 43-45.
- **Section starts:**
  - Sec 1 at p. 1, Sec 2 at 8, Sec 3 at 9, Sec 4 at 12;
  - **Sec 5 at 15-33** (5.1 at 18, 5.2 at 23; the new Lemma 5.28 and Theorem 5.29 at its end);
  - Sec 6 at 33;
  - Sec 7 at 36 (Proposition 7.1 = cor:main-free, then 7.1 Example at 38);
  - Sec 8 at 39, Sec 9 at 40, App A at 41.

### Integration: edit → place

| Edit / fix | Where in the slim |
|---|---|
| PART 1 (lem:plus-free-const, thm:plus-free, closing paragraph) | Replaces rem:plus-is (S 1007-1010) at the end of Sec 5.2. F1 applied (both replacements, verbatim). F10 applied: "Let p be an odd prime and κ ≤ 9 a divisor of p−1." now opens the statement |
| PART 2 (rem:plus-free-ten) | **Not adopted.** It is about 9 printed lines, against the limit of 6. rem:is-import (f) points to it by title (the full version's remark ``Class ten and beyond''). The κ = 11 sentence is kept in (f), and the F9 sentence goes with the remark to the full version |
| PART 3 | Inserted after the proof of Theorem main, before 7.1. **F2:** it is now `\begin{proposition}[The case $c \le 9$ of Theorem~\ref{thm:main}]` (the label cor:main-free is kept), and the F2 sentence is appended to "Correctness of the ideal procedure" (S 1085). **F7 adaptation:** the corollaries are in the full version, so "So do Corollaries …" became "So do the results (ii)-(iii) of Remark black-box for c ≤ 9, and (iv) for n ≤ 10", and the proof's last sentences now describe the full version's results (ii)-(iv) in the same terms, which the referee checked (obligation 3) |
| E1 | Abstract, verbatim |
| E2, E5b, E5c, E7a-c, E8, E12, E13a-b | No anchor: the text was cut in rounds 1-2 (informal statement, the second half of rem:main-solver, the old black-box paragraphs, rem:proof-uses, the scope remarks). E5c's content is in Sec 1.6 by F4 |
| E3 | thm:main hypothesis (S 181), with "Proposition" (F2) |
| F8 | thm:main (3): "for c ≥ 10 the t_{p,κ}" (applied; the referee called it optional) |
| E4 | S 206, verbatim |
| E5a, E6a, E6b | rem:main-solver and the imports paragraph, with "Proposition" |
| E9a, E9b | "What is new", adapted to the slim wording; same content |
| F3 | Related Work: "conditional on [IS15, Corollary 8], which rests on their Theorems 3 and 5" |
| E10 + F4 + F5 | Sec 1.6 "The exponents": F4's sentence opens the paragraph, and E10's sentence uses F5's wording ("three … programs", "refereed by a second (verdict: proved with fixes, applied here)") |
| E11 | rem:is-import (f) (S 557). Its "(and for c = 10, Remark plus-free-ten)" is replaced by the full-version pointer, since PART 2 was not adopted |
| F7 | rem:black-box: "each conditional only on Theorem is-import, and only for c ≥ 10 (for (iv), n ≥ 11; Proposition main-free), and (iii)-(iv) also on [II23, Theorem 1]" |
| E14a, E14b, F11 | Their paragraph ("Halving at the confirmed depth") moved to the full version (step 2), so neither is needed |
| E15 + F12 | New Appendix A row "Schedule 1H+ without candidate (a)", which names every program and the referee's `indep_isfree.py` and `kappa10_ref.py` |
| F6 | No anchor (E12 has none) |

### IS-dependent cuts (step 2)

- **rem:is-printed → full version.**
  - Sec 1.6 "The import" now states the confirmation itself: G. Ivanyos confirmed only the full-depth bound C(d,a) ≤ G(d,a)^{⌈log2(d+1)⌉} = B̄_d(a), and that the printed exponent of a+1 in [IS15, Thm 3] is a mistake. It gives the weaker 145 at c = 9.
  - It keeps "covers neither L_d, nor the halving, nor Sec 5.2, nor … 53, 38 and 20", and adds "for c ≤ 9, Theorem main and the exponent 20 do not use the import (Proposition 7.1)".
  - The references in rem:is-import (c), the Lemma rounds proof (S 583), the acknowledgment and Appendix A now name ``The printed bound'' of the full version.
- **The 95 / full-depth halving.** The Outlook paragraph and `pub_hcd.py` move to the full version, along with the "except for the halving at the confirmed depth" clause of the Outlook intro.
- **Proofs of 53 and 38 → pointers.** Lemma exponent (ii) and Lemma halved-exponent (ii) keep their statements (Theorem main (4) still states 53 and 38). Their proofs are pointers that name the method and the artifact, and both lemma statements now say the argument for (ii) is in the full version. The proofs of (i), of (iii) and of the inequalities A ≤ B and E_H ≤ E_1 stay verbatim, because Theorem main (4) and Lemma plus-exponent (iii) use them.
- **Dependency sentence (Sec 1.6).** It now reads: "Theorem main depends on the full version only for the proofs of Lemmas exponent(ii) and halved-exponent(ii), which give the stand-alone comparison values E_1(c) and E_H(c) of part (4), among them 53 and 38; every other proof it uses is given here."
- **"The exponents" reorganized.** In order: the F4 sentence for 20; the halving's referee history; Sec 5.2's history; the IS-free sentence (E10 + F5). It closes with: the stand-alone 53 and 38 rest also on Lemma rounds, Lemma zero-sum-length, Theorem is-import and the exact computations of Lemmas exponent(ii) and halved-exponent(ii), whose proofs are in the full version. Every verdict and "no human has read it" is kept.
- **Removed:** the 1H grade-profile paragraph at p ≡ 1 (mod 2520).
- **Kept for c ≥ 10:**
  - thm:is-import (stated);
  - rem:is-import (a)-(f);
  - the IS numbering, determinism and van de Woestijne paragraph;
  - Lemma rounds with its proof;
  - Lemma zero-sum-length with its proof;
  - Lemma bezout;
  - the Schedule 1 paragraph;
  - Lemma exponent (i).

### Not applied

- **PART 2** (about 9 lines, against the limit of 6).
- **Edits whose anchor was cut in rounds 1-2** (listed above), and with them F6 and F11.
- **A further move of Lemma rounds / zero-sum-length.** They are needed for c ≥ 10.

### Adversarial self-check (round 3)

- **Statements are verbatim** for the fragment, apart from:
  - F1: wording only;
  - F2: the environment type and title;
  - F10: the order of quantifiers;
  - F7: the slim adaptation of PART 3's corollary sentence, which now names Remark black-box (ii)-(iv). Those are the same four corollaries, and their scope is the referee's obligation 3.

  Theorem main changed only in its hypothesis (E3) and in F8.
- **No caveat dropped.**
  - The confirmation's scope moved into Sec 1.6, more explicitly than before.
  - The c ≥ 10 conditionality is stated at:
    - Theorem main;
    - the abstract;
    - rem:main-solver;
    - the imports paragraph;
    - What is new;
    - rem:black-box;
    - rem:is-import (f);
    - Proposition 7.1.
  - The note that the merged 1H+ fixes were not re-refereed is kept.
- **New dependency on the full version** (Lemmas exponent(ii) and halved-exponent(ii)). It is stated in Sec 1.6, and it concerns only the comparison values 53 and 38, never 20. Lemma plus-exponent (ii) cites halved-exponent (ii) only in its "new candidates switched off" comparison sentence, and plus-exponent (iii) uses halved-exponent (iii), which is kept.
- **Not verified:**
  - the mathematics of the fragment (I rely on the referee);
  - that the full version has the remarks ``The printed bound'' and ``Class ten and beyond'' and the full proofs of the (ii) parts (F2 gate);
  - the PDF beyond the build counts and greps.

## Round 4 (full-sync referee findings 2, 4, 5)

Labels: AI-checked, pending human review. No new mathematics; no claim strengthened. Template edit script `build/pass13.py`; backup `build/template.v15-pre-pass13.tex`.

- **Finding 4 (applied).** The EHK-replacement sentence in the "query separation" item (slim l.1072) now reads: "the bound on its query count is polynomial in $m$ of degree up to $E_+(c)$ and does not depend on $p$ once $p \ge 3/\eps$; we make no claim about the optimal quantum query complexity."
- **Finding 2 (not present).** No sentence in the slim says the combined rule (Schedule 2 with Schedule 1) gives smaller query counts. The full version's black-box outlook paragraph carrying it was cut in round 1. A grep for "smaller", "combined rule" and "Schedule~2" finds only the Extensions paragraph, which makes no such comparison. Nothing to change.
- **Finding 5 (not present / accurate).** The core:566 sentence ("Theorem main uses the smaller arity $B_d \le \bar B_d$") was inside rem:is-printed, which left the slim in round 3. The remaining "deterministic" and $B_d$ sentences concern Schedule 1 alone and are accurate: rem:main-solver (Schedule 1 alone is deterministic given its zero sums), rem:is-import(d) (with Schedule 1 alone only the zero sums are Las Vegas), and the Schedule 1 paragraph. No sentence says that Theorem main's procedure is deterministic or uses $B_d$.
- **rem:black-box (applied).** The corollaries now read as holding "for every $c$, using Theorem is-import only for $c \ge 10$ (for (iv), only for $n \ge 11$; Proposition cor:main-free), and (iii)–(iv) also assuming [ImranIvanyos2023, Theorem 1]". The doubled comma ",," is removed (0 left in the file).
- **Build.** 45 pp; 0 undefined references, 0 errors, 0 overfull boxes, 0 bib warnings.

Adversarial self-check:
- The "for every $c$" wording restates the round-3 integration of Proposition cor:main-free (Theorem main without the import for $c \le 9$). It is not a new claim. It still rests on the full version's black-box section, which this core does not prove.
- Finding 2 was checked by grep only. A paraphrase using none of the three search terms could have been missed. A manual read of the Outlook section (Section 9) found none.

## Round 5 (final referee, ACCEPT WITH FIXES)

Labels: AI-checked, pending human review. No new mathematics. The one statement change is a weakening (item 80 of the manifest).
- **Scripts:** `build/pass14.py` (fixes), `pass15.py` and `pass16.py` (cuts), using the new `fix`/`fixall` helpers in `build/tlib.py`.
- **Backups:** `template.v16-pre-pass14.tex`, `v17-post-pass14`, `v18-post-pass15`.
- **Result:** slim md5 `54b45724…`, 1130 lines. The referee's slim line numbers refer to the round-4 file `1eff5d12…`.

**Material findings**
- **M1.** The 38/53 clause has left thm:main(4). New Remark `rem:main-comparison` ("Comparison values; proved in the full version") sits right after thm:main. It states $E_H(9)=38$ and $E_1(9)=53$ as comparison values, proved in the full version and depending on Theorem is-import, and says that Theorem main does not use them.
  - Slim 186 gets the referee's text plus the pointer.
  - Sec 1.6 ("The exponents" and "Results of the full version") now points to the remark. The last sentence now reads "Theorem main does not use them, and every proof it uses is given here"; the referee checked that every other proof is given here.
  - The header "for c ≤ 9 no assumption is needed" is now accurate: part (4) keeps $E_+(9)=20$ and the inequalities, which are proved here.
- **M2.** The black-box sentence is deleted from the statement of cor:main-free, and the full-version call-structure sentence from its proof. Remark black-box now carries the referee's pointer to the full version's proposition "The case $c \le 9$ of Theorem main" (title checked: main.tex l.1745).
- **M3.** Applied as the integrator asked, without claiming the restriction argument:
  - Candidate (d) of Definition plus-schedule now reads "with $\Delta_t = \operatorname{lift}_{D_t}(\Omega_{t-1})$ for every $t$".
  - A new sentence after "depend only on (p,κ,a)" says that every chain of (b)–(d) and (f2) has $\Delta_t$ = lift. These are the chains the programs enumerate, so the stated arities and degrees are those of the candidates as defined. Corollary plus-chain allows larger $\Delta_t$, which Schedule 1H+ does not use.
  - Code checked: `plus2.py:118`, `plus_mine.py:311` and `indep_isfree.py:314` all set Δ = lift and require |Δ| ≥ 2. (b), (c) and (f2) are lift by inspection (Z_κ = lift(Z_1); {0,3,6} = lift_9({0})).
- **M4.** thm:plus-free(ii) now reads "$A^\circ = A^+$ for every a, and, if κ ≥ 2, $A^+ < G^{L}$"; the closing paragraph says "2 ≤ κ ≤ 9".
- **M5.** Proof overview layer (c): referee's text.
- **M6.** Ivanyos sentence: referee's text (C(d,a) removed; scope unchanged). The is-free history now says "applied here after that review and not re-refereed".
- **M7.** Abstract: referee's rewording, plus both removals. Length **1779 characters**: the source text of the abstract environment, comments stripped, ends trimmed; 283 words.
- **M8.** Now reads "in all three".

**Minor findings**
- **m1.1.** All 45 raw `\varepsilon` (the type parameter of Sec 5.1–5.2, thm:plus-free and rem:kappa-two) are now `\zeta`.
  - The error is `\eps` throughout and is untouched; only the `\newcommand{\eps}{\varepsilon}` line keeps `\varepsilon`.
  - ζ elsewhere appears only in Proposition dl-central-scalars (Sec 3.4, local).
  - The parameter is defined in Sec 5.1, so 5.1 is renamed too, for consistency.
- **m1.2.** Applied (lem:plus-free-const now uses $\mathcal I_D$, $N_D$, $K'_D$, $e'_D$).
- **m1.3.** The optional renamings are not applied.
- **m2.** Both forward references are fixed.
- **m3.** Section 5 retitled "Diagonal-Equation Solvers: Schedules 1, 1H and 1H+".
- **m4, m5.** Applied.
- **m6.** Pointers at 688, 956 and 195 now name targets by title; all titles were grepped in docs/papers/rees-hsp/main.tex (l.1371, 1499, 337). The pointer at 937 is superseded by cut 80, which names theorem "Uniform reversible compilation" (l.1481).
- **m7.** Adapted. After cut 80, von Staudt–Clausen is no longer used, so the import list adds only the Dynkin denominator bound, for Theorems rees-cover(iii) and uniform-compilation(i).
- **m8.** The proof of thm:plus-free now runs (i)–(ii), then (iii), with unchanged text.
- **m9.** `80256fcb` is replaced by `commit \ReesArtifactCommit{}`, and `\newcommand{\ReesArtifactCommit}{(to be set at release)}` is in the preamble (not numbers.tex). Release gate: the integrator sets it.
- **m10.** Lean paragraph unchanged; EllCheck is not imported by `Formal.lean`.

**Safe cuts** (manifest rows 77–84):
- the abstract;
- the M1 move;
- M2;
- uniform-compilation(i) (R5 item 10);
- classical-query (iii)–(iv) and the Nayak sentence (item 9, short form);
- the artifact table at folder level (item 8);
- the last sentence of rem:main-solver (item 5, light);
- the Related Work search protocol.

Not applied:
- **The roadmap and the move of rem:is-import(d)** (items 2–3): these reorganize and save nothing.
- **Moving the import list into Sec 1.6** (item 5 in full): Sec 1.6 has no such list, so this is a move, not a cut, and it risks dropping the exact-computation disclosure at slim 186.
- **Merging the Lean paragraph into a table row.**

**Build:** **44 pp** (was 45); 0 undefined references, 0 errors, 0 overfull boxes, 0 BibTeX warnings, 9 underfull boxes (ragged table).
- The referee's "3–4 pp" estimate (±30%) is not reached. The fixes add about 0.4 pp (the new remark, M3, M5, M2's pointer), and the listed cuts remove about 1.3 pp gross.
- Further options, not applied, for the integrator to decide:
  - Section 8 as one paragraph (about 0.3 pp);
  - the intro paragraph "Black-box groups and classical queries" (slim 188), which repeats rem:black-box and Sec 8 (about 0.2 pp);
  - a `\small` bibliography (about 0.4 pp).
- Caveat: `make.sh`'s section-page listing reads a stale `.toc`, since the document has no `\tableofcontents`; page positions were taken from the `.aux`.

Adversarial self-check:
- **Cut 80** changes a theorem statement. It is a weakening: an unspecified constant depending on d, instead of $(d-1)d(d+1)/2$. Theorem main(5) needs only $\mathrm{poly}_c$, and the Running time paragraph cites only "four BCH evaluations", which still holds.
  - The new proof relies on the proof of Theorem rees-cover(iii), via Dynkin's denominators for the truncation at degree ≤ d. Evaluating it monomial by monomial is routine, but this proof has not been refereed.
  - The full version's count is $(d-1)d(d+1)(d+2)/6$ (checked: main.tex l.1485). It is not $/2$, so the referee's suggested pointer for the $/2$ count would have been inaccurate. I did not use it.
- **M3:** whether (d) restricted to lift equals the referee's wider definition is exactly what the restriction argument would show. I did not claim it, and the definition now matches the code instead.
- **"Theorem main does not use them, and every proof it uses is given here"** rests on the final referee's check that only Lemmas exponent(ii) and halved-exponent(ii) came from the full version. I re-checked that thm:main(4) uses only part (i) and the inequalities of those lemmas.
- **The ε → ζ rename** was done by token. Every replaced line is in Sec 5.1–5.2 or thm:plus-free, by the referee's line list (my count also gives 45 occurrences on those 20 lines). The PDF was not visually inspected.

## Round 6 (integrator: the three optional cuts)

Labels: AI-checked, pending human review. No claim is changed. Manifest rows 85–87; script `build/pass17.py`; backup `template.v19-post-pass16.tex`.
- **Section 8:** the proposition is kept, with (i)–(ii) verbatim. The upper bound (iii) and the Θ statement are condensed, without weakening. The proof outline, the separation and all three limits are now one paragraph: not new (EHK); large constants and crossovers; queries to an oracle with arbitrary labels only, no explicit hard family, no concrete speedup.
- **Intro "Black-box groups and classical queries":** dropped. Every fact in it was checked against rem:black-box (i)–(iv), Proposition classical-query (i)–(iii) and the separation paragraph. Only the Organization sentence was extended, to name the separation.
- **Bibliography:** `\small`.
- **Round-4 copy:** `main-core-slim.round4.tex` was regenerated from `template.v16-pre-pass14.tex`. Its md5 `1eff5d12…` equals the final referee's target, so rounds 5–6 can be diffed against it.
- **Build:** **43 pp**; 0 undefined references, 0 errors, 0 overfull boxes, 0 BibTeX warnings, 9 underfull boxes (table).
- **Adversarial self-check:** the separation paragraph is long. The PDF was not visually inspected (pdftotext only), and the one-paragraph form was not re-refereed.

## Round 7 (round 5–6 referee, F1–F8)

Labels: AI-checked, pending human review. Script `build/pass18.py`; backup `template.v20-post-pass17.tex`.
- **F1:** abstract reworded as the referee wrote it.
- **F2(a)–(b):** applied as worded.
- **F3(a)–(b):** applied ("give"). For **F3(c)**, `\label{rem:query-separation}` was removed after grep confirmed it is unreferenced.
- **F5(a)–(b):** the stray blank lines in the longtable are deleted, and the second program is named.
- **F6:** the parenthesis is cut and the optional rewording applied.
- **F7(a):** applied.
- **F7(b):** applied by the referee's second route ("It also uses, …"). Its first route, the semicolon, would still leave two "and"s.
- **F8:** $N_D \to A'_D$ in Lemma plus-free-const, matching $K'_D$ and $e'_D$ (one occurrence).
- **F4 (record correction, not a slim change):** my Round 5 self-check on cut 80 was wrong. main.tex l.1485 states both "exactly $(d-1)d(d+1)(d+2)/6$" for the unoptimized schedule and "at most $(d-1)d(d+1)/2$" with stored coefficients, so the referee's /2 pointer would have been accurate. The slim text, which cites only the /6 count, is accurate either way and is unchanged.
- **Build:** **43 pp**; 0 undefined references, 0 errors, 0 overfull boxes, 0 BibTeX warnings, 9 underfull boxes (table).
- **Abstract:** **1808 characters** (source text of the environment, comments stripped).
- **Self-check:** the out-of-scope items (the two τ in Section 8, and the convention for input length) are not changed.
