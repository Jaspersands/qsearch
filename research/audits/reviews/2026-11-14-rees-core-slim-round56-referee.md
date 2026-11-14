# Hostile referee: slim Rees core, rounds 5 and 6 (2026-11-14)

AI only (one Claude Code referee agent), pending human review. Labels: PROVED, PROVED given cited theorems, CONDITIONAL, REFUTED, UNKNOWN, NOT computed.

- **Scope.** Only the changes between
  - `research/audits/reviews/2026-11-14-rees-core-slim/main-core-slim.round4.tex` (md5 `1eff5d12…`, the target of `…-core-slim-final-referee.md`, ACCEPT WITH FIXES), and
  - the current `…/main-core-slim.tex` (md5 `051d02bd…`, 1114 lines), written **slim N** below for line N.
- **Method.** A line diff (61 hunks) and a word-level diff (difflib on whitespace tokens; script in the session scratchpad, not kept). Every hunk was read against the final referee's exact old → new text and against the slimmer's account, `2026-11-14-rees-core-slim.md`, sections "Round 5" and "Round 6". Pointer targets were grepped in `docs/papers/rees-hsp/main.tex` and `appendix-*.tex` (18:38). The Δ = lift lines of the three programs were read.
- **Build.** A scratch copy in `2026-11-14-rees-core-slim/referee56-build/`, compiled with nice -n 19 (pdflatex, bibtex, pdflatex ×2).
  - **43 pp.**
  - 0 undefined references, 0 multiply defined labels, 0 overfull boxes, 0 LaTeX warnings, 0 errors, 0 BibTeX warnings.
  - 9 underfull boxes, all in the artifact longtable (source lines 1088–1098).
  - pdftotext shows no doubled words (the one "the the" is a `\widetilde G` extraction artifact) and no doubled punctuation.
- **Constraints.** No existing file edited, no Git commands, no network.

## Verdict: ACCEPT WITH FIXES

**Every final-referee fix is applied, and none is applied wrongly.** This covers M1–M8 and m1.1, m1.2, m2–m8 (m1.3 optional and not applied; m9, m10 handled as stated).

**The ε → ζ rename is exact.**
- In the round-4 file, 45 raw `\varepsilon` (46 minus the `\newcommand{\eps}{\varepsilon}` line) all became `\zeta`. All of them sit on the final referee's 20 lines, and every one is the type parameter.
- `\zeta` goes from 5 to 50 occurrences; the 5 old ones are all in Proposition dl-central-scalars (slim 362).
- No `\eps` (error) was touched. Its count drops from 43 to 42 only because the sentence "which does not depend on $p$ once $p \ge 3/\eps$" left the query-separation paragraph; that statement survives in the "First" limit (slim 1057) and after Theorem main (slim 187).
- Every `\eps` left in Sections 5.1–5.2 is the error budget of Remark is-import(d) (slim 485).

**The new proof of Theorem uniform-compilation(i) is correct and complete: PROVED given the cited Dynkin denominator bound.** Every later use still follows. No number in the paper rested on the removed count (d−1)d(d+1)/2.

**Section 8 claims nothing stronger than before.** All three limits are present, and part (iii) states the same upper bound.

**The round-5 and round-6 cuts leave no dangling reference and lose no caveat.**

**What remains is minor.** One item weakens the abstract's logic (F1). The rest are precision, record and cosmetic items. None changes a theorem's truth or strength.

## Checks performed (item by item)

**1. Final-referee fixes.**
- **M1 (applied correctly).** Theorem main(4) now ends `In particular $E_+(\ReesClassNineClass) = \ReesClassNinePlusExp$.` (slim 173). The new Remark `rem:main-comparison` (slim 180–183) sits directly after the theorem.
  - It states 38/53 as comparison values, proved in the full version and depending on Theorem is-import "read as statements about algorithms". It says that Theorem main does not use them.
  - Slim 192 carries the referee's text plus the pointer. Slim 220 and 222 point to the remark instead of part (4).
  - **The header "for c ≤ 9 no assumption is needed" is now honest.** Parts (3) and (4) contain only arity inequalities (A⁺ ≤ A ≤ B ≤ B̄ and E₊ ≤ E_H ≤ E₁ ≤ 1+Σ), the constants and E₊(9) = 20. All of these are proved here, the last by the exact computation of Lemma plus-exponent(ii). None of them is an algorithmic claim about Schedules 1 or 1H.
  - I checked that Lemmas exponent(ii) and halved-exponent(ii) (slim 544–551, 651–659) are the parts that state 53 and 38, and that their notes say "in the full version". The remark cites exactly those parts.
- **M2 (applied correctly).**
  - The black-box sentence is gone from the statement of cor:main-free (slim 1011), and the call-structure sentences are gone from its proof (slim 1015, which now ends "which $\mathcal H^\circ$ never runs.").
  - Remark black-box (slim 1035) carries the referee's pointer verbatim. Its target, proposition "The case $c \le 9$ of Theorem~\ref{thm:main}", exists at main.tex:1745.
- **M3 (applied as a restriction of the definition, consistently).**
  - Candidate (d) (slim 833) now requires $\Delta_t = \operatorname{lift}_{D_t}(\Omega_{t-1})$. The added sentence (slim 841) is accurate.
  - **(b) and (f2):** TL_κ = (κ, Z_κ, {0}) and U_m = (7, Z_7, {0,m}) over Gaussian elimination have Δ = lift_κ(Z_1) = Z_κ.
  - **(c):** TW = (9, {0,3,6}, {0}) over $\mathcal H^+_3$ has Δ = lift_9({0}) = {0,3,6}, by Table plus-thresholds (slim 750–757).
  - **(f3) and (fΩ):** these are chains of (d) by definition.
  - The p = 43 example in (d) satisfies the restriction: (7, Z_7, {0,1,2}) then (7, {0,1,2}, {0,2}), with lift_7({0,1,2}) = {0,1,2}.
  - Corollary plus-chain still requires |Δ_t| ≥ 2. So steps with lift = {0}, such as consecutive equal moduli after Ω = {0}, are excluded, as in the code: `plus2.py:118` (`if len(R) < 2: continue`), `plus_mine.py:311` and `indep_isfree.py:314`. I read all three.
  - **Consistency.**
    - Corollary plus-chain still proves the restricted chains (they are special cases).
    - Theorem plus(ii) runs them by that corollary.
    - Lemma plus-free-const bounds |Δ_t| − 1 ≤ κ − 1 for every step.
    - Lemma plus-exponent(ii) and Theorem plus-free evaluate the definition as now written.
    - The Lean modules formalize the more general chains, which covers the restricted ones.
- **M4 (correct).** Slim 906 reads `$A^\circ = A^+$ for every $a$, and, if $\kappa \ge 2$, $A^+ < G^L$`, and slim 928 reads "$2 \le \kappa \le 9$". The proof's base case "at $\kappa = 1$ both solvers are Gaussian elimination" (slim 914) matches the first clause.
- **M5–M8 (verbatim).** M5 is at slim 209, M6 at slim 218 and 220, and M8 at slim 928. For M7 (slim 62), the abstract is **1779 characters** (source, comments stripped) and 283 words, below arXiv's 1920. I recounted.
- **Minor findings.**
  - m1.2 is at slim 894 and 898; m2 at slim 721 and 813; m3 at slim 465 (texorpdfstring); m4 at slim 885; m5 at slim 187.
  - **m6.** The targets exist:
    - "Schedule 2: two-level symmetric contraction", main.tex:1371;
    - "Approximate Fourier transform over $\mathbb{Z}/N$ with explicit size", main.tex:1499;
    - "Related Work", main.tex:337;
    - "Uniform reversible compilation", main.tex:1481.
  - m7 is at slim 192, and m8 at slim 913–925.
  - **m9.** `\ReesArtifactCommit` renders "(to be set at release)". This remains a release gate.

**2. ε → ζ.** See the verdict. A grep for `\epsilon` and Unicode ε finds nothing. No type-parameter occurrence written as `\eps` exists anywhere: I listed and classified all 42 `\eps` occurrences, and every one is an error or precision parameter.

**3. Theorem uniform-compilation(i), new proof (slim 944, 951).**
- **The steps check out:**
  - By the argument of rees-cover(iii) with d in place of c (Khukhro, Remark 9.17), Dynkin's formula writes BCH_d as a Z[1/d!]-combination of right-normed Lie monomials of length ≤ d. Each coefficient's denominator divides n·N·∏ r_i! s_i! with n, N ≤ d.
  - On a class-≤ d algebra over F_p with p > d, the product BCH_c agrees with BCH_d, because all terms of degree > d vanish. This holds on G_d, which is a quotient of (A, ∗) by Lie homomorphisms.
  - A length-k monomial costs k − 1 brackets, and the number of terms depends only on d.
  - The divisions are only by those denominators. The vector work is O_d(1) scalings and additions.
- **What the weakened statement still supports:**
  - Theorem main(5) (poly_c gates);
  - the Running-time paragraph (slim 1007: "four BCH evaluations by Theorem (i)–(ii)");
  - Theorem uniform-compilation(ii), unchanged;
  - Lemma copy-lift;
  - the error composition, which uses only part (iii), unchanged.
- **No number is lost.** A grep for brackets, recurrences, (d−1)d…, Bernoulli, von Staudt and `uniform_bch` finds no other use of the explicit count. The new pointer is accurate: main.tex:1485 says "In this unoptimized schedule this uses exactly $(d-1)d(d+1)(d+2)/6$ bracket evaluations".

**4. Section 8 (slim 1044–1059).**
- Proposition (i) and (ii) are verbatim.
- **(iii) states the same upper bound with the same Q.** "Outputs a subalgebra of $\hh$" keeps the one-sidedness of the old "the output is always contained in $\hh$", and "for every H" and "poly(Q, m, log p) further work for fixed c" are kept.
- The Θ sentence is unchanged in content.
- **The separation claim is unchanged:** a ratio of at least $p^{(m-1)/2}/\poly_c(m)$, for fixed c and $p^{m-1}\to\infty$.
- **The three limits are all present:**
  - First, not new (EHK), with no claim of optimality;
  - Second, large constants and crossovers, and the 1H⁺ threshold not computed;
  - Third, queries to an oracle with arbitrary labels only, no explicit hard family, no concrete speedup.
- The EHK HUMAN-VERIFICATION comment is kept.
- What was lost is only the old remark's strengthening "even when H is promised non-normal of order p". That loss is not a caveat. See F3 for two precision points.

**5. Cuts.**
- **Proposition classical-query (iii)–(iv).** Nothing cites (iii)–(v) of the old numbering. The only reference left is `prop:classical-query}(i)` (slim 1059). The proof outline now points to the full version for both lost bounds, and main.tex:1815–1816 and appendix-classical-proof.tex hold them.
- **The intro paragraph "Black-box groups and classical queries".** Each of its facts is still stated:
  - the reductions and corollaries, in Remark black-box (i)–(iv);
  - the lower and upper bounds, in Proposition classical-query (i)–(iii);
  - the separation and its limits, in slim 1057–1059;
  - "no speedup for any concrete problem" and "no application", in slim 201, 1035, 1059 and the abstract.
- **The Related Work sentence.** The search protocol is described in full at main.tex:337ff (Semantic Scholar, OpenAlex, INSPIRE-HEP, OpenCitations, the keyword search). "Not exhaustive" is kept.
- **The abstract.** The black-box sentence and the "±1" clause are removed; see F1.
- **The artifact table at folder level.** It loses no premise. See F5.

**6. Build.** See the header.

## Findings (slim line; exact old → new)

**F1. The abstract's "public ones need not exist" no longer has its justification** (slim 62).
- M7's cut of "and its automorphisms scale its centre only by ±1" leaves only "has no positive grading". A missing grading excludes dilations, but not other automorphisms that scale the centre. The fact that carries the claim is Proposition dl-central-scalars, and the intro has both facts (slim 77).
- The fix is about +20 characters, giving roughly 1800 < 1920.
  - old: `and public ones need not exist: the class-three Dixmier--Lister algebra has no positive grading over $\Fp$ ($p > 3$).`
  - new: `and public ones need not exist: the automorphisms of the class-three Dixmier--Lister algebra over $\Fp$ ($p > 3$) scale its centre only by $\pm1$.`
- (This applies the referee's own M7 suggestion; the gap is mine to flag, not the slimmer's error.)

**F2. Theorem uniform-compilation(i): two precision points** (slim 944, 951).
- **(a) Dimension.** L itself has dimension m ≤ D_c, not D_d. This wording predates round 5, but it sits in the rewritten item, and the full version says "at most".
  - old: `any Lie algebra of class at most $d$ and dimension $D_d$`
  - new: `any Lie algebra of class at most $d$ and dimension at most $D_d$`
- **(b) The proof of rees-cover(iii) is written for c.**
  - old: `(i) By the proof of Theorem~\ref{thm:rees-cover}(iii), the truncation $\BCH_d$ is a fixed Lie polynomial`
  - new: `(i) By the proof of Theorem~\ref{thm:rees-cover}(iii) with $d$ in place of $c$, the truncation $\BCH_d$ is, by the Dynkin formula, a fixed $\mathbb{Z}[1/d!]$-linear combination of Lie monomials of length at most $d$, and is in particular a Lie polynomial`
  - The rest of the sentence ("in $X, Y$ with coefficients in $\mathbb{Z}[1/d!]$, …") is unchanged. "Monomial by monomial" presupposes such a representation, and the Dynkin form is the one whose coefficients are bounded termwise.

**F3. Section 8: two precision points** (slim 1052, 1057).
- **(a) "The birthday algorithm" is not defined in the core.** The old statement defined it, so (iii) is not weaker, but it is less self-contained. One clause restores it:
  - old: `The birthday algorithm with $Q = \dots$ independent uniform queries outputs`
  - new: `The birthday algorithm, which makes $Q = \dots$ independent uniform queries and outputs the Lie subalgebra generated by $\log(x^{-1}x')$ over all pairs of queried points $x, x'$ with equal labels, outputs`
  - Here $\dots$ stands for the unchanged formula for $Q$.
- **(b) "this gives" has no explicit antecedent** inside a paragraph that also contains the proof outline.
  - old: `With Theorem~\ref{thm:main}, whose count`
  - new: `Proposition~\ref{prop:classical-query}(i) and~(ii), with Theorem~\ref{thm:main}, whose count`
  - Also adjust `this gives` → `give`.
- **(c) Cosmetic.** `\label{rem:query-separation}` (slim 1057) now sits on a `\paragraph`. It resolves to "8", and nothing references it. Either delete it or leave it.

**F4. Record error in the slimmer's Round 5 self-check** (`2026-11-14-rees-core-slim.md`, Round 5, "Cut 80"). It says the full version's count "is not /2, so the referee's suggested pointer for the /2 count would have been inaccurate".
- main.tex:1485 states both: "exactly $(d-1)d(d+1)(d+2)/6$" for the unoptimized schedule, and "at most $(d-1)d(d+1)/2$ bracket evaluations suffice" with the stored $W^{(k)}_o$.
- The paper's text is accurate either way. Only the record is wrong.
- Optionally, the slim could keep the sharper count as a pointer: `; the full version evaluates it by a recurrence with exactly $(d-1)d(d+1)(d+2)/6$ bracket evaluations, and at most $(d-1)d(d+1)/2$ with stored coefficients (theorem ``Uniform reversible compilation'')`.

**F5. Artifact table** (slim 1091–1096).
- **(a) Stray blank lines.** There are three empty source lines inside the longtable after the 1H⁺ row (slim 1092–1094). They are harmless in the PDF, but the integrator should delete them.
- **(b) The is-free row names "the third program" but never the first two.** Theorem plus-free (slim 928) says three programs. The round-4 row identified the second as `ref20_copy/dump_noS1.py`.
  - old: `on the helpers in \file{R/2026-11-14-rees-core-plus-referee/}; the third program in`
  - new: `on the helpers in \file{R/2026-11-14-rees-core-plus-referee/}; the second program is \file{ref20_copy/dump_noS1.py} there; the third is in`

**F6. Duplication that is safe to cut** (slim 192).
- The parenthesis `($\ReesClassNineHalvedExp$ with Schedule~1H alone and … Remark~\ref{rem:main-comparison})` repeats Remark main-comparison eight lines earlier.
- The sentence `The values $E_+(9)=20$, $E_H(9)=38$ and $E_1(9)=53$ … also use exact computations` lists 38/53 among the things "the proof" uses, although Theorem main does not use them. Optional fix: `The value $E_+(\ReesClassNineClass) = \ReesClassNinePlusExp$ and $C^+_c = C_c$ for $c \le 9$ also use exact computations (Lemma~\ref{lem:plus-exponent}; the comparison values of Remark~\ref{rem:main-comparison} also rest on Lemmas~\ref{lem:halved-exponent} and~\ref{lem:exponent})`.

**F7. Wording** (slim 200, 192).
- **(a)** "Our literature search covered … the 2023--2026 arXiv literature on the hidden subgroup problem" reads as complete coverage. It was a keyword search (main.tex:345).
  - old: `the 2023--2026 arXiv literature on the hidden subgroup problem and`
  - new: `a keyword search of the 2023--2026 arXiv literature on the hidden subgroup problem, and`
- **(b)** The import list has a double "and": "…, and Bennett's reversible simulation of classical circuits~\cite{Bennett1973}, and, for Theorems…".
  - old: `the subgroup form of the Lazard correspondence, a standard`
  - new: `the subgroup form of the Lazard correspondence; a standard`
  - The other route is to turn the last item into a separate sentence: `It also uses, for Theorems … (i), the denominator bound of the Dynkin formula …`.

**F8. Optional notation** (slim 894). $N_D(a)$ in Lemma plus-free-const reuses the letter of $N_p$ (Definition plus-rc) and of $N_d$, the number of merges (slim 997). This is harmless in context.

## Out of scope (pre-existing, not changed in rounds 5–6; listed only)
- Section 8 uses two τ: τ = ⌈log_p(3/ε)⌉ from Theorem main in the separation paragraph, and τ = ⌈log_p(2/ε)⌉ in Proposition classical-query(iii).
- "exponential in the input length $m\log_2 p$" takes the input length to be the bit length of a group element, not the m³ log p bits of the structure constants. That is a reasonable convention for an oracle problem, and it predates round 4. The paper could say "the bit length $m\log_2 p$ of a group element".

## Adversarial self-check
- **Could a hunk have been missed?** The word diff covers all 61 hunks of `diff` (162 changed lines), and I read each one. The table rows were compared at folder level. I did not open every artifact folder to confirm that it still contains what the row claims.
- **The new compilation proof** is short, and my check relies on the standard form of the Dynkin formula and on the cited Khukhro remark, which I did not reopen. If Khukhro's remark bounded only the coefficients of the Lie polynomial and not the termwise Dynkin denominators, the "monomial by monomial" step would need F2(b)'s representation argument. The Dynkin formula's own coefficients make that argument immediate. PROVED given the cited bound.
- **M3.** I verified the definition against the code and the table, not the claim that the restriction changes no arity. That is the final referee's argument, which the paper no longer needs, since the definition now matches the code.
- **F1 might be pedantic.** The intro states both facts. But an abstract claim followed by a colon and an insufficient reason is a logical slip, and it costs about 20 characters to repair.
- **Not checked:** the visual PDF layout (pdftotext only); the bibliography entries; the full-version content behind the titled pointers beyond their titles and the two statements quoted (main.tex:1485, 1815–1816); the exact computations, which are unchanged since round 4.
