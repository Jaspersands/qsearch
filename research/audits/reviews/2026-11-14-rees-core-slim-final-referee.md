# Final hostile referee: slim 45-page Rees core (2026-11-14)

AI only (one Claude Code referee agent), pending human review. Labels: PROVED, PROVED given cited theorems, CONDITIONAL, REFUTED, UNKNOWN, NOT computed.

- **Target:** `research/audits/reviews/2026-11-14-rees-core-slim/main-core-slim.tex` (md5 `1eff5d12…`, 1132 lines), written **slim N** below for line N. I read the paper cover to cover before opening any report.
- **Reports consulted afterwards:**
  - `2026-11-14-rees-core-slim.md` (rounds 1–4);
  - `…-core-slim-referee.md`;
  - `…-is-free-referee.md`;
  - `…-core-plus-referee.md`;
  - the Lean 1H+ review;
  - the full version `docs/papers/rees-hsp/main.tex` (18:27), for pointer targets only.
- **Build:** a scratch copy in `2026-11-14-rees-core-slim-final-referee/build/`, compiled with nice -n 19 (pdflatex, bibtex, pdflatex ×2).
  - **45 pp.**
  - 0 undefined references, 0 overfull boxes, 0 BibTeX warnings.
  - 10 underfull boxes, all in the ragged artifact table (slim 1106–1116).
  - The PDF text (`slim.txt`) has no doubled words and no doubled punctuation.
- **Constraints:** no existing file edited, no Git commands, no network. Only the compile was run.

## Verdict: ACCEPT WITH FIXES

**The main line is correct and complete in this document.** I re-derived it by hand:
- Sections 3–4, Proposition descent, the error budget (ε/3 + ε/3 + ε/3) and the hybrid lemma;
- the Las Vegas abort split (ε/6 + ε/6);
- the counts N_solver and N_QFT;
- Lemmas rounds, zero-sum-length, two-term, stage, finish, plus-refine, plus-chain, plus-sm, plus-tensor, plus-ell-node, plus-stage and plus-finish;
- the lower bounds of Lemmas exponent(i), halved-exponent(i) and plus-exponent(i), including 19 + (⌈c/2⌉² − 25) + 2(⌊c/2⌋ − 4) + 1 = 20 at c = 9;
- lem:plus-free-const (superadditivity of f, the strict comparison with G(κ,a)^L);
- the induction of thm:plus-free, including the (5,4) case (ε = 1, T_2 = F_5^×, degree 5 ≤ 12, constant 1 < 4^18);
- Proposition cor:main-free.

These are PROVED given the cited theorems (Weil, Rabin, Chevalley–Warning, Dirichlet for the lower bounds) and the cited exact computations.

**No number is wrong.** I checked by hand:
- 145;
- 20 = 1 + 5·2 + 3·3 at p ≡ 1 (mod 2520);
- 38 = 1 + 37 from the 1H profile;
- the class-three counts 4320 ≈ 2^12.08, 209,952 ≈ 2^17.68 and 13,436,928 ≈ 2^23.68;
- 49·(2·10^6)^7 < 10^46.

**What needs fixing.** Eight findings are material. None changes a theorem's truth, but each makes the text claim more than it proves, contradict itself, or misstate a quantifier:
- M1: Theorem main(4) states two values that this core does not prove, and their algorithmic reading needs the import;
- M2: Proposition cor:main-free asserts full-version results;
- M3: Definition plus-schedule(d) now quantifies over more chains than the computations enumerate;
- M4: thm:plus-free(ii) is false or undefined at κ = 1;
- M5: the proof overview is stale;
- M6: the Status section has an undefined symbol and an inconsistent referee-history label;
- M7: the abstract overstates one claim and exceeds the arXiv length limit;
- M8: "in both" is stale.

## Material findings (slim line; exact old → new)

**M1. Theorem main(4) contains claims that are delegated and conditional, under a header that says "no assumption" for c ≤ 9.** (slim 154, 173, 186, 217)
- Part (4) ends: "Schedule 1H alone gives E_H(9) = 38, and Schedule 1 alone E_1(9) = 53".
- Both values are proved only in the full version (slim 217, 545, 653).
- Read as statements about algorithms, both need Theorem is-import at c = 9: Schedules 1 and 1H run candidate (a) at odd κ (Remark main-solver, slim 183: "both use Theorem is-import").
- The theorem's header says "for c ≤ 9 no assumption is needed". So Theorem main is not fully proved in this document, and one caveat is lost inside the theorem itself. The inequalities E_+ ≤ E_H ≤ E_1 ≤ 1 + Σ… are proved here and stay.
- **Fix, slim 173:**
  - old: `In particular $E_+(\ReesClassNineClass) = \ReesClassNinePlusExp$; Schedule~1H alone gives $E_H(\ReesClassNineClass) = \ReesClassNineHalvedExp$, and Schedule~1 alone $E_1(\ReesClassNineClass) = \ReesClassNineQueryExp$.`
  - new: `In particular $E_+(\ReesClassNineClass) = \ReesClassNinePlusExp$.`
- **Fix, slim 186:**
  - old: `($\ReesClassNineHalvedExp$ with Schedule~1H alone, $\ReesClassNineQueryExp$ with Schedule~1 alone)`
  - new: `($\ReesClassNineHalvedExp$ with Schedule~1H alone and $\ReesClassNineQueryExp$ with Schedule~1 alone; both schedules use Theorem~\ref{thm:is-import}, and these two values are proved in the full version)`
- **Fix, slim 217:**
  - old: `which give the stand-alone comparison values $E_1(c)$ and $E_H(c)$ of part~(4), among them`
  - new: `which give the stand-alone comparison values $E_1(c)$ and $E_H(c)$ stated after Theorem~\ref{thm:main}, among them`

**M2. Proposition cor:main-free asserts results that the core does not prove.** (slim 1012, 1016, 1036)
- The statement ends: "So do the results (ii)–(iii) of Remark black-box for c ≤ 9, and (iv) for n ≤ 10."
- Its proof ends with a description of the full version's call structure.
- Remark black-box itself says "this core does not prove them". A proposition of the core should state only what the core proves. I checked the full version: cor:black-box, cor:black-box-pe, cor:nilpotent and cor:utz carry "if c ≥ 10 (n ≥ 11) assume", so the content is right but misplaced.
- **Fix, slim 1012:** delete ` So do the results~(ii)--(iii) of Remark~\ref{rem:black-box} for $c \le 9$, and~(iv) for $n \le 10$.`
- **Fix, slim 1016:** delete the final two sentences, from ` In the full version, the black-box results~(ii)` to `uses Theorem~\ref{thm:is-import} otherwise.`
- **Fix, slim 1036:**
  - old: `(for~(iv), only for $n \ge 11$; Proposition~\ref{cor:main-free})`
  - new: `(for~(iv), only for $n \ge 11$; in the full version this follows from its proposition ``The case $c \le 9$ of Theorem~\ref{thm:main}'', since~(ii) calls Theorem~\ref{thm:main} at class at most $c$, (iii) calls~(ii) and~\cite[Theorem~1]{ImranIvanyos2023}, and~(iv) calls~(iii) at class $n-1$)`
- This saves about 4 lines.

**M3. Definition plus-schedule(d) now ranges over more chains than the exact computations enumerate.** (slim 709, 828, 836, 880)
- Corollary plus-chain was weakened from Δ_t = lift to **Δ_t ⊇ lift_{D_t}(Ω_{t−1})** (refereed: full-sync referee, Lean review). That is correct.
- But candidate (d) is "every chain … of Corollary plus-chain", so the candidate set grew.
- The programs behind Lemma plus-exponent(ii) and Theorem plus-free use Δ = lift exactly:
  - `plus2.py:118`;
  - `plus_mine.py:311`;
  - `indep_isfree.py:314`.
- So the computation does not literally evaluate the definition as written.
- **No arity changes, and this is PROVED by restriction.**
  - A contraction for (D,Δ,Ω) restricts to one for (D, lift, Ω): drop the β_i with i ∉ lift. The conditions are per i, and α_0 + β_0 is unchanged.
  - The smaller Δ has a smaller arity factor (|Δ|−1)a+1 and the same Ω_t.
  - If the lift is {0}, then D_t = D_{t−1} and Ω_{t−1} = {0}. The step can then be dropped: the preceding node is already an Ω_t-node of smaller arity, and the later steps stay valid because lift(Ω_{t−1}) ⊆ lift(Ω_t) ⊆ Δ_{t+1}.
  - It cannot be the only step: D_0 = D_1 = κ would contradict D_0 < κ, and a Gaussian base has lift = Z_{D_1}.
  - Plans and finishes are monotone in node arity, and the constants of lem:plus-free-const only decrease.
- **Fix, slim 836, after `So $A^+_\kappa(a)$ and $e^+_\kappa$ depend only on $(p,\kappa,a)$.`, insert:** `A chain with $\Delta_t \supsetneq \operatorname{lift}_{D_t}(\Omega_{t-1})$ changes no arity: restricting $\beta$ to $\operatorname{lift}_{D_t}(\Omega_{t-1})$ gives a contraction for the smaller step, of smaller arity and with the same $\Omega_t$, and when that lift is $\{0\}$ the step can be dropped, since the node before it is already an $\Omega_t$-node of smaller arity. The computations of Lemma~\ref{lem:plus-exponent} and Theorem~\ref{thm:plus-free} therefore take $\Delta_t = \operatorname{lift}_{D_t}(\Omega_{t-1})$.`

**M4. thm:plus-free(ii) is false or undefined at κ = 1.** (slim 898, 901, 921)
- The theorem is stated for "κ ≤ 9 a divisor of p−1", so κ = 1 is included.
- There t_{p,1} is undefined (slim 150 defines t only for κ ≥ 2). Read naively (t = 2, L = 1), the inequality A°_1(a) = a+1 < G(1,a) = a+1 is false.
- The proof's induction uses only "same arities" at D = 1, so nothing breaks.
- **Fix, slim 901:**
  - old: `\item $A^\circ_\kappa(a) = A^+_\kappa(a) < G(\kappa,a)^{\lceil\log_2 t_{p,\kappa}\rceil}$ for every $a \ge 0$.`
  - new: `\item $A^\circ_\kappa(a) = A^+_\kappa(a)$ for every $a \ge 0$, and, if $\kappa \ge 2$, $A^+_\kappa(a) < G(\kappa,a)^{\lceil\log_2 t_{p,\kappa}\rceil}$ for every $a \ge 0$.`
- **Fix, slim 921:**
  - old: `So at $\kappa \le 9$ candidate~(a)`
  - new: `So at $2 \le \kappa \le 9$ candidate~(a)`

**M5. The proof overview is stale after round 3.** (slim 204)
- Layer (c) says that the Ivanyos–Santha collision step, together with the halving and the contractions, "supply the solutions". For c ≤ 9 it is never run.
- **Fix:**
  - old: `The Ivanyos--Santha collision step, iterated $L_d$ times and closed with the shortest zero sum of $\kappa_d$-th powers, and, at even $\kappa_d$, the halving of Section~\ref{sec:halving}, which turns a solver for the exponent $\kappa_d/2$ into one for $\kappa_d$ by keeping two representations of one vector, and the contractions of Section~\ref{sec:plus}, which combine solutions whose weights lie in prescribed cosets of the $\kappa_d$-th powers, supply the solutions for arbitrary labels at arity $A^+_d(g_d)$.`
  - new: `The halving of Section~\ref{sec:halving}, which turns a solver for the exponent $\kappa_d/2$ into one for $\kappa_d$ by keeping two representations of one vector, and the contractions of Section~\ref{sec:plus}, which combine solutions whose weights lie in prescribed cosets of the $\kappa_d$-th powers, supply the solutions for arbitrary labels at arity $A^+_d(g_d)$; for $c \ge 10$ the solver also uses the Ivanyos--Santha collision step, iterated $L_d$ times and closed with the shortest zero sum of $\kappa_d$-th powers, which for $c \le 9$ is never run (Theorem~\ref{thm:plus-free}).`

**M6. Status section: an undefined symbol, a self-contradictory "only", and an inconsistent referee label.** (slim 213, 215)
1. **C(d,a) is used once and never defined, and "confirmed only X (he also confirmed Y)" contradicts itself.** The fix keeps Ivanyos's scope exactly: the bound fix of Theorem 3, nothing else.
   - old: `has confirmed only the full-depth bound $C(d,a) \le G(d,a)^{\lceil\log_2(d+1)\rceil} = \bar B_d(a)$ of the proof of~\cite[Theorem~3]{IvanyosSantha2015} (he also confirmed that the exponent of $a+1$ printed in~\cite[Theorem~3]{IvanyosSantha2015} is a mistake; see the full version, remark ``The printed bound''), which with Schedule~1 alone gives`
   - new: `has confirmed only the bound fix for~\cite[Theorem~3]{IvanyosSantha2015}: the exponent of $a+1$ printed there is a mistake, and its proof gives the full-depth arity $G(d,a)^{\lceil\log_2(d+1)\rceil} = \bar B_d(a)$ (the full version, remark ``The printed bound''). With Schedule~1 alone this gives`
2. **The is-free history is labelled less carefully than the 1H+ history.** The referee's F7 adaptation and PART 3 were rewritten by the slimmer, and no referee saw the integrated text before this report.
   - old: `it was written by one AI session and refereed by a second (verdict: proved with fixes, applied here), and no human has read it.`
   - new: `it was written by one AI session and refereed by a second (verdict: proved with fixes, applied here after that review and not re-refereed), and no human has read it.`
   - The owner may instead cite this report.
3. **Accurate as written:**
   - the halving history (three sessions, correct with fixes);
   - the 1H+ history (drafts 21 and 20, each PROVED WITH FIXES; merged write-up CORRECT WITH FIXES, "applied here after that review and not re-refereed"). I checked it against the headline-21, headline-20 and core-plus referee verdicts.
   - Ivanyos is credited only for the bound fix: slim 213, 1124 and the acknowledgement.

**M7. The abstract overstates one claim and is too long.** (slim 61)
- **Overstatement.** "fewer evaluations do not suffice for every H" reads as a query lower bound. Remark fewer-points (slim 316) says explicitly that it "concerns the pullback construction, not the number of queries any algorithm needs".
  - old: `which every graded dilation preserves; fewer evaluations do not suffice for every $H$.`
  - new: `which every graded dilation preserves; with fewer evaluation points the pulled-back subgroup is not dilation-invariant for every $H$.`
- **Length.** The abstract is 330 words and 2045 source characters, above arXiv's limit of 1920. Remove the black-box sentence ("Corollaries in the full version …") and the clause "and its automorphisms scale its centre only by ±1" (about 330 characters).

**M8. A stale "in both".** (slim 921) The degrees now come from three programs.
- old: `the only pair with $e^\circ_\kappa > \kappa$ in both.`
- new: `the only pair with $e^\circ_\kappa > \kappa$ in all three.`

## Minor findings

**m1. Notation.** Each item is safe to apply mechanically.
1. **ε is printed twice.** `\eps` (the error) and the type parameter `\varepsilon = -q^{-1}` print the same glyph, sometimes in the same section (Remark is-import(d) and Section 5.1).
   - Replace the raw `\varepsilon` at slim 569, 573, 579, 595, 597, 599, 603, 607, 617, 642, 797, 801, 805, 808, 830, 833, 850, 874, 880 and 918 by `\zeta`. All 20 are the type parameter. ζ occurs elsewhere only in the local Proposition dl-central-scalars (slim 357).
2. **lem:plus-free-const reuses Schedule 1H symbols** (slim 889): $\mathcal H_D$, $A_D$, $K_D$ and $e_D$ belong to Schedule 1H, while the lemma is applied to $\mathcal H^\circ$ and $\mathcal H^+$.
   - old: `let the inner solvers $\mathcal H_D$ ($D \mid \kappa$, $D < \kappa$) of the candidates of Definition~\ref{def:plus-schedule} at $\kappa$ have arities $A_D(a) \le K_D(a+1)^{e_D}$, with $(e_1,K_1) = (1,1)$ and $K_D \le (D-1)^{f(e_D)}$ for $D \ge 2$.`
   - new: `let the inner solvers $\mathcal I_D$ ($D \mid \kappa$, $D < \kappa$) that the candidates of Definition~\ref{def:plus-schedule} at $\kappa$ use in place of $\mathcal H^+_D$ have arities $N_D(a) \le K'_D(a+1)^{e'_D}$, with $(e'_1,K'_1) = (1,1)$ and $K'_D \le (D-1)^{f(e'_D)}$ for $D \ge 2$.`
   - Then change `from these $e_D$ and $K_D$` to `from these $e'_D$ and $K'_D$`, and `inner solvers $\mathcal H_D$` (proof, slim 893) to `inner solvers $\mathcal I_D$`.
3. **Optional renamings:**
   - the type tuple $c = (c_1,\dots,c_r)$ clashes with the class c (slim 563–830);
   - G = G(d,a) clashes with the group G (slim 469, 490);
   - ξ is overloaded: the coset generator, ξ_q (slim 1028), Z(ξ) (slim 944) and the state ξ (slim 968).

**m2. Forward references.** H^+_3, e^+_3 (slim 716) and H^+_{κ/2} (slim 808) are used before Definition plus-schedule.
- **Slim 716:**
  - old: `$(\mathcal H^+_3;(9,\{0,3,6\},\{0\}))$ has degree $e^+_3 + 1$.`
  - new: `$(\mathcal H^+_3;(9,\{0,3,6\},\{0\}))$, with the solver $\mathcal H^+_3$ of Definition~\ref{def:plus-schedule} below, has degree $e^+_3 + 1$.`
- **Slim 808:**
  - old: `$\mathcal N = \mathcal H^+_{\kappa/2}$ (a $\{0,\kappa/2\}$-node at modulus $\kappa$)`
  - new: `$\mathcal N = \mathcal H^+_{\kappa/2}$ (Definition~\ref{def:plus-schedule} below; a $\{0,\kappa/2\}$-node at modulus $\kappa$)`

**m3. Section 5's title is stale** (slim 460). It covers Schedules 1, 1H and 1H+; the earlier referee's readability item 1 was not applied.
- old: `\section{Schedule 1: The Ivanyos--Santha Solver}`
- new: `\section{\texorpdfstring{Diagonal-Equation Solvers: Schedules~1, 1H and~1H$^+$}{Diagonal-Equation Solvers: Schedules 1, 1H and 1H+}}`
- This keeps 5.1 = sec:halving and 5.2 = sec:plus.

**m4. "values below" (slim 880):** 3 and 5 are equal to the values listed, not below them.
- old: `and values below those listed for $c \le 8$.`
- new: `and values at most those listed for $c \le 8$.`

**m5. An undefined phrase** (slim 179):
- old: `a coset generator and coset representatives, coset contractions and finite tables`
- new: `a coset generator, coset contractions and finite tables`

**m6. Pointers that do not name their target by title.** All other "full version" pointers resolve: I grepped every quoted title in main.tex and appendix-*.tex at 18:27, and all exist, including "The printed bound", "Class ten and beyond", "The grades at the maximizers" and "The exponent of Schedule 1H+".
- **Slim 688:**
  - old: `these are the two-level contractions of Schedule~2 in~\fullv; we use`
  - new: `these are the two-level contractions of \fullv\ (subsection ``Schedule 2: two-level symmetric contraction''); we use`
- **Slim 937:**
  - old: `implements and the full version counts, uses exactly`
  - new: `implements and the full version counts (theorem ``Uniform reversible compilation''), uses exactly`
- **Slim 956:**
  - old: `\fullv\ also gives an explicit construction of the Fourier transform over $\mathbb{Z}/N$, for odd $N$, with the same guarantee`
  - new: `\fullv\ also gives, in its lemma ``Approximate Fourier transform over $\mathbb{Z}/N$ with explicit size'', an explicit construction for odd $N$ with the same guarantee`
- **Slim 195:** `(full version, Related Work)` → `(full version, subsection ``Related Work'')`.

**m7. "Its only imported ingredients" omits two cited facts** (slim 186): Dynkin's denominator bound (slim 273) and von Staudt–Clausen (slim 952). After `Bennett's reversible simulation of classical circuits~\cite{Bennett1973}` insert `, and, for Theorems~\ref{thm:rees-cover}(iii) and~\ref{thm:uniform-compilation}(i), the denominator bound of the Dynkin formula~\cite[Remark~9.17]{Khukhro1998} and the von Staudt--Clausen theorem`.

**m8. thm:plus-free's proof is in the wrong order** (slim 908–918). It proves (iii) first and then says "This uses (i)". Put "(i) and (ii)." first; the text is unchanged.

**m9. Release gate: Appendix A** (slim 1097). Commit `80256fcb` predates every 2026-11-13/14 folder cited in the table and `formal/Formal/Schedule1HPlus/`. These are untracked in the session git status, and the repository is public. The ARXIV-TODO must be resolved before any posting.

**m10. Lean paragraph** (slim 1121). It is accurate for `formal/Formal/Schedule1HPlus/`. The Lean review's `Schedule1HPlusReview/EllCheck*.lean` kernel-checks all five tables of Proposition plus-tables but is not imported by `Formal.lean`. If the owner integrates it, delete "Proposition~\ref{prop:plus-tables}," from the "Not formalized" list and say so. Otherwise leave the paragraph unchanged.

## Readability: the 10 most valuable improvements

1. **M1:** move the 38/53 comparisons out of Theorem main(4). This makes the theorem self-contained and shorter.
2. **m3:** retitle Section 5, and open 5.2 with a four-line roadmap. Candidates (a)–(f) are S1, TL, TW, TB, L and plans. At large p their degrees are (e^+_1,…,e^+_9) = (1,2,2,2,2,2,3,3,3) (slim 876). Readers meet nine pages of 1H+ without a map.
3. **Move Remark is-import(d)** (slim 480, about 22 lines) into Section 7 as `\paragraph{Las Vegas steps and the abort budget.}` and repoint its six references (slim 183, 991, 993, 1008, 1016 and Theorem plus-free).
   - It is the error budget of the main proof. It sits inside a remark about the IS import, which c ≤ 9 no longer uses.
   - Remark is-import keeps (a)–(c), (e) and (f).
4. **M5:** fix the proof overview's layer (c).
5. **One home for the import list and the exponent provenance.** Today it is stated at slim 179, 183 (end of Remark main-solver), 186 and 213–217.
   - Keep the list in Sec 1.6.
   - Reduce slim 186 to its first two sentences and a pointer.
   - Delete the last sentence of Remark main-solver.
   - This saves about 0.3 pp.
6. **m1.1:** rename the type parameter ε to ζ. It is the most confusing clash in Section 5, because the error ε appears in the same section.
7. **M7:** cut the abstract to about 1850 characters.
8. **Appendix A at folder level.** Compress the table to one row per result, listing folders rather than every script; the folders hold READMEs.
   - Merge the Lean paragraph into one row and keep its "not formalized" list.
   - This saves about 0.8 pp.
9. **Section 8.** Drop Proposition classical-query (iii) and (iv), which nothing in the slim cites, along with the Nayak sentence (about 0.3 pp). Alternatively, reduce the section to one paragraph plus Remark query-separation (about 1 pp), since the separation is "not new".
10. **Theorem uniform-compilation(i).** Replace the Bernoulli recurrence (slim 944–952) with "BCH_d is a fixed Lie polynomial over Z[1/d!] (Theorem rees-cover(iii)); evaluate it monomial by monomial", and point to the full version's theorem "Uniform reversible compilation" for the (d−1)d(d+1)/2 count. Theorem main(5) needs only poly_c. This saves about 0.4 pp.

**Further safe cut:** about 3–4 pp (to about 41–42 pp) from items 5, 8, 9 (short form), 10, M2, M7 and a 0.3-pp condensation of Related Work. That rises to about 5 pp if Section 8 shrinks to one paragraph.
- None of these touches the proof chain of Theorem main: Sections 3–4, 5.1–5.2, 6, 7 up to Proposition 7.1, and the lemmas they cite.
- Not recommended: dropping Schedule 1H (Section 5.1). Definition plus-schedule runs its plans "as in Definition schedule1h", and Lemma plus-exponent(iii) uses c_κ from Lemma halved-exponent(iii).

## Typography and LaTeX

- 0 undefined, 0 overfull, 0 errors, 0 BibTeX warnings, 45 pp.
- The only remaining doubled punctuation is the harmless `$k! $` (slim 952); the ",," of round 4 is gone.
- No odd spacing was found in the PDF text. I could not render pages (pdftoppm is absent), so the visual layout is NOT checked.
- Every "full version, …" pointer names a title, except slim 688, 937 and 956 (m6), and every titled target exists in the full version at 18:27.

## Adversarial self-check

- **Could I have missed an error in the main line?** I re-derived the proofs listed in the verdict. I did **not** recompute:
  - Table plus-thresholds;
  - 1−Φ(p_D);
  - the 4·10^14 and 10^46 constants beyond order of magnitude;
  - Lemma plus-sm's second-moment constants beyond the structure of the argument;
  - the exact computations of Lemma plus-exponent(ii)/(iii) and Theorem plus-free. Three programs and two referees agree on these.

  Those inherit AI-only status. The full-version proofs (53, 38, Proposition dl-central-scalars, Proposition classical-query) were not read.
- **M3 might be immaterial.** It is, numerically: my restriction argument shows no arity changes. It is listed because the paper's exact-computation claims would otherwise evaluate a definition that differs from the code. The argument is mine and unrefereed.
- **M4 might be pedantic.** κ = 1 is plainly intended to be excluded, but the statement as printed asserts a false strict inequality there. The fix costs ten characters.
- **M1 might be too strict, since Sec 1.6 already says that 38/53 rest on the full version and the import.** But a theorem whose header says "no assumption for c ≤ 9" should not contain an algorithmic claim that needs the import. The cheap fix moves one clause.
- **The p = 307 capped searches.** The is-free referee reported e^+(307,9) UNKNOWN in {3,4} because of three capped searches. The core-plus referee had already resolved those three steps as NONE with a larger cap (`cap307.out`), so "exhaustive search for p ≤ 600" (slim 880) is accurate. I did not rerun it.
- **Page estimates** are by eye from the label page map (aux), ±30%.
- **Not checked:** the visual PDF layout; that the full version's titled targets contain the cited content, not just the titles; the bibliography entries.
