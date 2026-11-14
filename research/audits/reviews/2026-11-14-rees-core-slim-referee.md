# Hostile referee: slim 44-page core draft (2026-11-14)

This review is AI only (one Claude Code referee agent) and is pending human review.

- **Target.** `research/audits/reviews/2026-11-14-rees-core-slim/main-core-slim.tex` (written **slim** below). It was generated at 17:36:02 from `build/template.tex`, which was modified at 17:35:59.
- **Baseline.** `2026-11-14-rees-full-sync/core-snapshot-68pp.tex` (written **S** below). Its md5 is `71743611…`, the same as `docs/papers/rees-hsp/core/main-core.tex` and `orig-main-core.tex`.
- **Line numbers.** "slim N" is line N of `main-core-slim.tex`, and "S N" is line N of the snapshot.
- **Compilation.** I recompiled a scratch copy (nice -n 19; pdflatex, bibtex, pdflatex ×2): **44 pp.**, 0 undefined references.
- **Helpers.** The word-diff helper and the sentence-level "new text" list are in `2026-11-14-rees-core-slim-referee/` (`wd.py`, `newsent.txt`).
- **Constraints kept.** I edited no existing file. I ran no Git command and used no network.

## Verdict: ACCEPT WITH FIXES

The cuts keep every hypothesis of Theorem main, in all parts and for all three exponents.
- I checked every theorem, lemma, proposition and definition with the same label in S by machine: each is **verbatim**.
- The only exceptions are remarks and Theorem uniform-compilation, which lost part (iv), the memory bound. Nothing cites (iv).
- The proof of Theorem main (slim 972-989), the error composition (slim 943-965) and Sections 3-4 are verbatim.
- All of Section 5.2 (Schedule 1H+) is verbatim, apart from the condensed proof of Theorem plus (ii), the prime lists and Remark plus-profile.
- The Ivanyos caveat is kept: "confirmed only the full-depth bound … covers neither the shorter depth L_d, nor the halving, nor Section plus" (slim 221). Nothing claims more for it.

Six findings are material (F1-F6). None changes a theorem, but four of them make the text inaccurate as it stands:
- F1: the dependency sentence in Sec 1.6 is wrong;
- F3: a newly printed claim is false in one regime;
- F4: one intro claim lost its support;
- F6: one reference dangles.

F2 is a release gate. F5 is a status upgrade that the slimmer's report does not list.

---

## Material findings

**F1. The core defers more of Theorem main's algorithm than Sec 1.6 says.** (Q1; slim 225, 639, 864, 488, 989)
- Slim 225 says: "Theorem main depends on the full version only for the details of the proofs of Lemmas zero-sum-length and exponent".
- But the parts (ii) of Thms halving and plus now end with "an explicit polynomial, whose recursion is written out in the full version" (slim 639) and "a recursion, written out in the full version, that defines the bound T^+_κ" (slim 864).
- That T is load-bearing. Remark is-import(d) cuts each solver attempt off after 4T steps (slim 488), and the running-time paragraph of the main proof uses "4T(M_d, log p) … with T the polynomial of Theorem plus(ii)" (slim 989).
- So the procedure of Section 7 is not fully specified inside the core.
- The cut saved only about 10 lines: the tail of S 733 from "Explicitly, let R_κ(p) bound …" to "this recursion defines T.", and the tail of S 969 from "Explicitly, with R_κ(p) and T_κ …" to "… depending only on κ, because every inner arity is at most A^+_κ(a).".

Fix:
1. Restore both "Explicitly, …" passages verbatim from S 733 and S 969 (about 0.3 pp), replacing the sentences "by induction its expected time is bounded by an explicit polynomial, whose recursion is written out in the full version" (slim 639) and "Over the finitely many … this gives a recursion, written out in the full version, that defines the bound …" (slim 864).
2. Recommended: also restore the full proof of lem:zero-sum-length (S 596-605, about +0.3 pp over the sketch). It serves every c, it gives the Las Vegas trial probabilities used in the cut-offs, and the sketch is already about 60% of its length.
3. Then rewrite slim 225:
   - old: `Theorem~\ref{thm:main} depends on the full version only for the details of the proofs of Lemmas~\ref{lem:zero-sum-length} and~\ref{lem:exponent}, which are sketched here.`
   - new (if both restorations are made): `Theorem~\ref{thm:main} depends on the full version only for the details of the proof of Lemma~\ref{lem:exponent}, which is sketched here; they give the values $E_1(c)$, among them $\ReesClassNineQueryExp$, and the bound $E_1(c) \ge c(c+1)/2$.`
   - new (if nothing is restored): `Theorem~\ref{thm:main} depends on the full version for the details of the proofs of Lemmas~\ref{lem:zero-sum-length} and~\ref{lem:exponent}, which are sketched here, and for the explicit running-time recursions of Theorems~\ref{thm:halving}(ii) and~\ref{thm:plus}(ii), which define the cut-offs of Remark~\ref{rem:is-import}(d).`

**F2. Gate: the "full version" pointers point into a file that does not yet contain their targets.** (Q1/Q3)
- `docs/papers/rees-hsp/main.tex` and `appendix-*.tex`, read at about 17:40, have none of: `\label{thm:halving}`, `thm:plus`, `def:plus-schedule`, `sec:plus`, `lem:halved-exponent`, `lem:plus-exponent`, `rem:plus-profile`, `\ReesClassNinePlusExp`, or the recursions "R_\kappa(p)" / "this recursion defines".
- These slim pointers therefore lead nowhere today:
  - slim 639 and 864 (the recursions);
  - slim 892 (the per-prime lists and the single-m exceptions);
  - slim 894 ("28 primes (listed in the full version)");
  - slim 897 (profiles at the six exceptional primes).
- The targets of these slim pointers do exist in main.tex: slim 361 and 368 (Dixmier–Lister), 554 (53: `2521, 7561, 12601` and `v_2(p-1)` are present), 1036 (`lem:collision`), 1046 (`tab:query-crossover`), 918 (`(d+1)(d+2)/6`), 937 (odd N) and 1008 (the corollaries).
- The slimmer said the full version is being prepared (the full-sync helper is still writing at 17:41).
- Fix and acceptance test: before any release, grep the synced full version for each slim pointer target listed above. Give section numbers, not "the full version", for slim 639, 864, 892, 894, 897 and 1036.

**F3. The restored EHK sentence is a new printed claim, and it is false in one regime.** (Q2; slim 1044)
- In S, the sentence "Theorem main adds polynomial running time at polynomially many queries; it does not lower the query count, and its count is far above the information-theoretic one" sits inside a `% NEEDS HUMAN VERIFICATION` comment (S 1346), so it is not printed. The slim prints it.
- The slim's own bound shows the problem. Q_q ≤ c(m+τ)∏B̄_d(g_d) is independent of p once p ≥ 3/ε (slim 1042), whereas the EHK count is O(log²|G| + log(1/ε)) = O(m² log² p).
- So at fixed m and c, with p → ∞, the bound of Theorem main is the smaller one, and "does not lower the query count" fails.
- "The information-theoretic one" is undefined.

Fix (old → new):
- old: `Theorem~\ref{thm:main} adds polynomial running time at polynomially many queries; it does not lower the query count, and its count is far above the information-theoretic one.`
- new: `Theorem~\ref{thm:main} adds polynomial running time; its query count is polynomial in $m$ of degree up to $E_+(c)$ and does not depend on $p$ once $p \ge 3/\eps$, and we make no claim about the optimal quantum query complexity.`

Apply the same fix to main-core.tex if the integrator un-comments that sentence there.

**F4. An intro claim lost its support.** (Q3; slim 79 vs slim 1002)
- Obstacle (2) still says: "In the free two-generator class-three Lie algebra over F_5, every subgroup is preserved by automorphisms that scale the centre … (Section example-class3)".
- The only support was the S 1138 sentence "Over F_5, the stabilizer of every subgroup of G acts on the centre by every cube (exact computation)", which the slim cut.
- Slim 1002 now shows such automorphisms only for the one H = exp(F_p v).

Fix: insert, after "…scales the centre by θ³." in slim 1002:
- `Over $\mathbb{F}_5$, the stabilizer of every subgroup of $G$ acts on the centre by every cube (exact computation).`
- Add its artifact to the Appendix A table; it is listed in S 1381-1412.

**F5. A status upgrade that the slimmer's report does not list; the main core is stale on the same point.** (Q2; slim 223)
- S 257 and S 787 say "The write-up of Section plus, which merges the two drafts, has not itself been refereed".
- Slim 223 says it "was refereed by a further AI session (verdict: correct with fixes, all applied here)". Slim 682 drops the clause.
- The report (17:35:11) predates the template change (17:35:59). Its old/new list omits this change, and its Finding 3 ("kept verbatim even though it may be stale") no longer describes the draft.
- I checked the new wording against `2026-11-14-rees-core-plus-referee.md`:
  - the verdict there is CORRECT WITH FIXES;
  - its fixes F2, F3, F4, F5, F6, F8, F9 and F10 are present in S and in the slim (for example "consecutive moduli may be equal", "odd prime $p < 2\cdot10^6$", "$\max(2\cdot10^6, 4\kappa^4)$", "guarantees only above", "Section~\ref{sec:plus}, or the exponents");
  - F7 and F9 sit in condensed text.
- So the upgrade is supported by the records. That referee did, however, write "I did not diff all 1469 lines against the 08:45 text" after the 09:02 collision.

Fix:
1. Keep slim 223, made precise:
   - old: `was refereed by a further AI session (verdict: correct with fixes, all applied here); no human has read it.`
   - new: `was refereed by a further AI session (verdict: correct with fixes, applied here after that review and not re-refereed); no human has read it.`
2. Apply the same change to main-core.tex S 257 and S 787, which are stale.
3. Delete the stale source comments at slim 671-676 (also S 776-781: "this merged write-up has NOT been refereed", "draft subsection … to be \input …"). The arXiv source is public.

**F6. A reference dangles.** (Q3; slim 871)
- Slim 871 says "reads 'not available' from the lists in the proof of Lemma plus-exponent". Those lists were cut (slim 892 gives counts only).
- old: `and reads ``not available'' from the lists in the proof of Lemma~\ref{lem:plus-exponent}.`
- new: `and reads ``not available'' from the lists of the artifacts (Appendix~\ref{app:artifacts}).`

---

## Minor findings (wording and pointers)

**F7.** The macro `\fullv` (slim 48) prints "the full version (Appendix A)". Appendix A is this core's artifact list, so slim 700 ("Schedule 2 in the full version (Appendix A)") and slim 937 mislead.
- old: `\newcommand{\fullv}{the full version (Appendix~\ref{app:artifacts})}`
- new: `\newcommand{\fullv}{the full version (ancillary file \file{anc/rees-hsp-full.pdf})}`

**F8. The Ivanyos caveat, made explicit.** In the original, F10 of the plus referee named the exponents; slim 221 dropped them and kept a reading that is ambiguous.
- old: `which with Schedule~1 alone gives the weaker exponent $1+\sum_{d=2}^c d\lceil\log_2(d+1)\rceil$ ($145$ at $c = 9$), and $95$ with the halving (Section~\ref{sec:outlook}). His confirmation covers neither the shorter depth $L_d$, nor the halving, nor Section~\ref{sec:plus}.`
- new: `which with Schedule~1 alone gives the weaker exponent $1+\sum_{d=2}^c d\lceil\log_2(d+1)\rceil$ ($145$ at $c = 9$); combined with the halving, which it does not cover, that bound gives $95$ (Section~\ref{sec:outlook}). His confirmation covers neither the shorter depth $L_d$, nor the halving, nor Section~\ref{sec:plus}, nor, therefore, the exponents $\ReesClassNineQueryExp$, $\ReesClassNineHalvedExp$ and $\ReesClassNinePlusExp$.`

**F9. Abstract claims proved only in the full version.** The abstract states "its automorphisms scale its centre only by ±1" and "the classical randomized query complexity is Θ(p^{(m−1)/2})". Their proofs are now only pointed to (slim 368, 1036).
- Prop dl-central-scalars (slim 363), old: `[Central scalars of $\mathcal{L}_{\mathrm{DL}}$; AI-checked, pending human review]`
- new: `[Central scalars of $\mathcal{L}_{\mathrm{DL}}$; proof in the full version]`
- Prop classical-query (slim 1019), old: `[Classical query complexity]`
- new: `[Classical query complexity; proof in the full version]`

**F10. Remark black-box drops promises and oracle conditions of the corollaries** (slim 1008, against S 1172, 1196, 1238, 1269).
- In (ii):
  - old: `For a black-box $p$-group of class $c<p$ with unique encoding and a coherent multiplication oracle, of any exponent,`
  - new: `For a black-box group with unique encoding and a coherent multiplication oracle, promised (not tested) to be a $p$-group of class $c<p$, of any exponent, with $p$ given,`
- In (iii):
  - old: `the same guarantee holds for every black-box nilpotent group of fixed class with unique encoding, of any order,`
  - new: `the same guarantee holds for every black-box group with unique encoding and a coherent multiplication oracle, promised (not tested) to be nilpotent of class at most $c$, of any order,`
- In (iv):
  - old: `hidden subgroups of finite index in $\UT_n(\mathbb{Z})$`
  - new: `hidden subgroups of index at most $2^b$ in $\UT_n(\mathbb{Z})$, with time polynomial in $b$,`

**F11.** Remark is-import(c) (slim 487) lost the zero sum that makes the recovery deterministic.
- old: `Lemma~\ref{lem:rounds} with $t = d+1$ recovers it`
- new (the S 555 text): `Lemma~\ref{lem:rounds} with $t = d+1$ and van de Woestijne's zero sum recovers it`

**F12.** Related Work (slim 195) lost a caveat that limits a claim (S 222).
- old: `is not covered here). The growing-prime`
- new: `is not covered here); the bounds of those papers are not implied by ours. The growing-prime`

**F13. Stale source comment.** The comment at slim 1045 still contains the printed sentence and `\ref{tab:query-crossover}`, a label that no longer exists. Delete the tail after "…not checked." The `ARXIV-TODO` commit `80256fcb` (slim 1073) predates the 2026-11-14 artifact folders that the table cites (this is inherited from S).

Wording changes checked as **equivalent or weaker** (Q2):
- abstract (corollaries "in the full version");
- obstacle (1);
- Dixmier–Lister "12-dimensional over Q": the old family has 4 + 4·2 = 12 free parameters;
- rem:is-printed bases sentence;
- rem:query-separation (b), checked against the crossover arithmetic: p = 29, from N₁ = p²+p+1 against C(32,2); p = 61, from C(q,2) ≥ (2/3)N₁ − 1 with Q_q = 4320;
- "exponential in the input length" (slim 1042);
- Outlook status;
- the "What is new" non-awareness sentence: the slim refers to Lazard p-groups, S to any groups, so the slim is narrower;
- the Lean paragraph: "no unconditional algorithm for κ ≥ 3" is covered by "Not formalized: … root extraction".

Strengthened: only F3 and F5, plus the omissions of F10-F12.

---

## Readability (Q4): the five worst rough edges

1. **Section 5's title, "Schedule 1: The Ivanyos–Santha Solver", covers 16 pp (16-32).** Of these, 9 pp are Schedule 1H+ and have no roadmap. Rename it "Diagonal-Equation Solvers: Schedules 1, 1H and 1H$^+$" with a 5.0 "Schedule 1". Open 5.2 with a five-row table of the candidates (a)-(f) and their degrees at large p, (1,2,2,2,2,2,3,3,3) (slim 888). It can replace prose.
2. **The intro opens (slim 72) with Lazard, gradings, dilations and diagonal equations before the HSP is defined** (slim 76). Swap the first paragraph with the first paragraph of 1.1, or start 1.1 directly.
3. **About 20 bare "in the full version" pointers with no section numbers, plus the `\fullv`/"Appendix A" confusion (F7).** A referee cannot find the deferred proofs. Use section numbers once the full sync lands (F2).
4. **Remark free23** (slim 199-202, about 0.5 pp) sits in Related Work. It is "not a result of this paper" and nothing uses it, yet a referee meets it exactly where novelty is assessed. **Remark black-box** (slim 1006-1009) sits in Section 7, after the worked example, where it is out of place.
5. **The same import, exponent and status content appears three times:** the paragraph after Thm main (slim 188), Remark main-solver (slim 185) and Sec 1.6 (slim 219-225). The proof overview's (c) (slim 212) is a single 90-word sentence.

The proof overview does match the sections: lift is §3, descent §4, solve and compile §§5-6, assemble §7. The intro still motivates (obstacles 1-2, Heisenberg example, interpolation).

---

## Further slimming (Q5)

Estimates are in printed pages. Every item is safe for soundness provided Theorem main's proof chain (slim 972-989 and what it cites) is untouched.

| # | Cut | Saves | Soundness note |
|---|---|---|---|
| 1 | Drop the table of contents (slim 64-65) | ~0.5 | none |
| 2 | Move rem:free23 to the full version; one sentence in obstacle (2) and Related Work ("for this one group a cover-free algorithm, not reviewed by a human and not used here, is in the full version") | ~0.45 | nothing uses it |
| 3 | Condense Related Work (slim 195-197) to the BCvD + IS composition, II23, and the dated search sentence | ~0.6 | keep the scope-only and "not implied" caveats (F12) |
| 4 | Merge Prop single-evaluation into rem:fewer-points (its k = 1 case already says it); drop the F_3 example (slim 320) | ~0.25 | update the reference at slim 122 |
| 5 | Thm uniform-compilation (i): replace the Bernoulli recurrence (slim 925-933) with "BCH_d is a fixed Lie polynomial over Z[1/d!] with O_d(1) bracket monomials (Thm rees-cover(iii)); evaluate it term by term", and move the bracket count to the full version | ~0.5 | Thm main(5) needs only poly_c |
| 6 | Sec 7.1: keep the cover, the non-normal line and Automorphisms (plus F4); cut "Stages three and two" to two sentences | ~0.35 | illustrative |
| 7 | Delete rem:black-box; keep the intro paragraph (slim 190) and the abstract clause; repoint Open problem (4) and slim 197 to "the full version" | ~0.35 | nothing depends on it |
| 8 | Classical section: keep Prop (i), (ii) and (v) and rem:query-separation; drop (iii) and (iv) (cited nowhere in the slim) and the Nayak line | ~0.3 | not used by Thm main |
| 8′ | Alternative to 8: move all of Sec 8 to the full version, keeping one paragraph in the intro and the abstract sentence marked "(full version)" | ~1.2 | the separation is "not new" |
| 9 | Outlook to 4 sentences (Schedule 2 / triangular / Schedule 3 exist conditionally; the 95; open problems) | ~0.5 | none |
| 10 | Delete the slim 188 imports paragraph; Sec 1.6 and rem:main-solver already carry it | ~0.3 | keep the list once, in Sec 1.6 |
| 11 | Appendix A: merge the Lean paragraph into one table row | ~0.3 | keep every "not formalized" item |

Total: **about 4.5 pp, or about 5.5 pp with 8′**, giving about 38-39 pp. That partly offsets F1, which adds about 0.6 pp back.

**If the parallel helper's result (Thm main at c ≤ 9 without Theorem is-import) is proved and refereed.** It is currently CONDITIONAL; it rests on the computation of rem:plus-is, which can only falsify, plus a proof.
- **Restatement.** Thm main would read "unconditional for c ≤ 9; assuming Thm is-import for c ≥ 10". Lemma rounds, Lemma zero-sum-length, Thm is-import, rem:is-import (a)-(c), (e) and the Schedule 1 paragraph must stay for c ≥ 10, because at odd κ ≥ 11 candidate (a) is the only candidate.
- **What could move to the full version:**
  - rem:is-printed and the B̄_d links in Thm main(3), slim 152 and slim 181 (~0.35). The uniform-in-p bound follows from the B_d bound of Lemma exponent.
  - Lemma exponent (ii) (the E_1 values and 53) and the "53" clause of Thm main(4); keep (i) (~0.4).
  - Lemma halved-exponent (i)-(ii) (the 38), keeping (iii)'s c_κ definition, which Lemma plus-exponent(iii) uses, and the paragraph at slim 668 (~0.7).
  - The Outlook's 95 paragraph (~0.15).
  - The "exponents" paragraph of Sec 1.6 and rem:main-solver, which shrink to the c ≥ 10 caveat (~0.3).
- **Total.** About 2 pp. Lemma plus-exponent's first sentence and its (ii) last sentence ("switched off … values of Lemma halved-exponent(ii)") need rewiring.
- **Not recommended.** Restricting the core to c ≤ 9 would save about 2.5 pp more, but it would drop the "for every fixed c" headline from the core. That is the owner's call.

---

## Adversarial self-check

- **Did I miss a hypothesis change?** The verbatim check (label-matched environment comparison with whitespace normalized) covers statements only. Remarks were compared by word diff on about 25 lines, not all 77 lines that `newsent.txt` flags. Many of those flags are line-join artifacts, but I did not read every one, so a lost qualifier inside a condensed remark or paragraph is possible. The highest residual risk is in slim 195-204 and 1056-1064.
- **Is F3 right?** Yes. It rests on the slim's own statement that the bound is p-independent for p ≥ 3/ε and on the EHK count quoted in slim 1044. The EHK count is an upper bound, so "does not lower" is a comparison of bounds and fails as one. I did not check EHK beyond the slim's own quotation.
- **F5 relies on records, not re-refereeing.** I confirmed the presence of the fix strings, not that each applied fix is mathematically correct.
- **F2 is time-dependent.** The full-sync helper may already have added the targets after 17:40. Re-run the grep.
- **F1 severity.** One could argue that a recursion "of finitely many polynomial-cost steps" defines T well enough. I treat explicitness as required, because Remark is-import(d) runs the cut-off at 4T and so needs T to be computable.
- **Page estimates** are by eye from the 44-page PDF and the label page map, ±30%.
- **Not checked:** the full version's mathematics; the correctness of the plus-referee fixes; the PDF layout beyond the TOC and the page map.
