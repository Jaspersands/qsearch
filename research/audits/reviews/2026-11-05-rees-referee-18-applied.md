# Referee 18 (core): application record

Source report: `research/audits/reviews/2026-11-05-rees-referee-18-core.md` (0 Error, 0 Gap, 6 Imprecision, 6 Style).
Edited file: `docs/papers/rees-hsp/core/main-core.tex` only. `core/references.bib`, `core/numbers.tex`, `main.tex` and the appendices are untouched (another agent is restructuring `main.tex`). Backup of the pre-edit core and bib: `/private/tmp/claude-501/-Users-jaspersands-Developer-qsearch/6a6cfdd7-c9d4-4169-9805-7e18625bbdd7/scratchpad/bak_r18/`. Full diff: `.../scratchpad/r18.diff` (same folder).

Applied 5 November 2026 by an AI session; every change is AI-checked only, pending human review. No proof changed. No `\label` was renamed or removed; one label was added (`sec:related`). "AI-checked, pending human review" occurs 12 times before and after. NEEDS HUMAN VERIFICATION comments: 2 before, 3 after (new one on EHK). No new `\mathsf`, `\mathrel`, `\begingroup`, `\aa`, `\ni`. `make_numbers.py` was not run.

## Build and test

- Scratchpad build (`build_r18`, `latexmk -g -pdf`): **27 pages** (26 before), 0 Overfull, no undefined references or citations, no multiply defined labels, no "Float too large".
- `/opt/anaconda3/bin/python -m pytest -q tests/tools/test_rees_paper_numbers.py`: 2 passed (the test checks `numbers.tex` and the macros of `main.tex`; the core's number macros are unchanged).

## Findings

| # | Class | Verified? | Decision |
|---|---|---|---|
| 1 | Imprecision | Yes. `main.tex` `rem:combined-schedule` ("Block-steered option") and rule (R1) of `appendix-free-coordinate.tex` use $J_d = \max(3,\kappa_d)$ blocks, at grades with $2 \le \kappa_d < p-1$; $M_J(a) = \lfloor(a+2)^2/4\rfloor + [a\text{ odd}]$ at $J = 3$ and $a^2/(2(J-1)) + O(a)$ in general (`rem:sde-block-steered`). The core's "$\kappa_d \le 3$" included $\kappa_d = 1$ (division by zero). | **Applied, reworded.** Referee's "$\kappa_d \ge 3$" overlapped the $\{2,3\}$ case; I wrote "in general" with $J_d - 1$, and added the range $2 \le \kappa_d < p-1$. |
| 2 | Imprecision | **Referee's recollection is wrong.** The local arXiv text of EHK (`research/audits/reviews/2026-11-02-rees-classical-lower-bound/refs/quant-ph_0401083.txt`) has Theorem 1: $O(\log^4\lvert G\rvert)$ queries, exponentially small error (exact in a model with arbitrary one-qubit gates); Theorem 2: $\Pr[H\mid H] \ge 1 - 4r/2^{s/2}$, so $s \in \Theta(n^2 + \log(1/\eps))$, $n = \log\lvert G\rvert$; exponential running time (Section 2.1). $O(\log\lvert G\rvert)$ appears there only for the one-sided *decision* problem (concluding remarks). The old core sentence was correct. | **Rejected as proposed; softened and flagged.** Kept $O(\log^2\lvert G\rvert + \log(1/\eps))$ with Theorem 2, made the error explicit, added Theorem 1, and added a `% NEEDS HUMAN VERIFICATION` comment (IPL numbering unchecked). |
| 3 | Imprecision | Yes: $t$ was both the Rees variable and the sample surplus (theorem, Lemma 2.1, Section 7, Heisenberg example, Prop. 8.2(v), Table 1 caption). | **Applied.** Surplus renamed to $\tau$ at all 32 occurrences (scripted with exact-count assertions, then a token scan confirmed every remaining $t$ is the Rees variable: $t^k$, $t\mathcal{L}$, $t\hh$, $\mathcal{L}[t]$, $t$-degree, $tx$, $tz$). The ODE parameter in the proof of Theorem 6.1(i) was $\tau$; renamed to $\xi$ (11 occurrences; $\xi$ elsewhere is only the bound state in Lemma 6.2). Prop. 8.2(v)'s own surplus $\lceil\log_p(2/\eps)\rceil$ also became $\tau$. |
| 4 | Style | Yes. | **Applied, reworded** (see final text below). Same content: hypotheses, output, error, query count, displayed bound, gate count; the explicit bound is its own item. "Evaluation points $1,\dots,c$ and Schedule 1 with $M_d = B_d(g_d)$" moved to the sentence after the theorem, with the consequence "polynomial in $m$ for fixed $c$, independent of $p$ once $p \ge 3/\eps$". Added the one-sentence informal version before the theorem, and one sentence relating the result to Ivanyos–Santha after Remark 1.3. |
| 5 | Style | Yes. | **Applied, reworded.** 283 → 247 words. Referee's draft kept as base; restored "when $\mathcal{L}$ is not abelian" (needed for the non-normal claim), "Conditional extensions are described in an outlook", and named the IS solver as an imported theorem. |
| 6 | Imprecision | Yes: Prop. 4.3 applies $\delta_{s_i}$; Remark 5.2(a) already says so. | **Applied** in Remark 1.3. |
| 7 | Imprecision | Yes: `rem:fc-witness-h3`(c) and `main.tex` line ~788 use, at $\kappa_d = p-1$, the node of `rem:fc-zero-sum-arity`(b) or Schedule 1. $\kappa_d = p-1$ forces $p-1 \mid d \le c < p$, so $d = p-1 = c$. | **Applied, reworded:** "Schedule~1 or another public node of the full version at a grade with $\kappa_d = p-1$ (which occurs only for $p = c+1$ and $d = c$)". |
| 8 | Style | Yes ($\gamma_2 = \Span(e_5,\dots,e_8)$, $\gamma_3 = \Span(e_7,e_8)$ from the brackets). | **Applied** with $\gamma_k(\mathcal{L}_{\mathrm{DL}})$ notation. |
| 9 | Style | Yes, "Lazard $p$-group" was undefined. | **Applied** in Preliminaries; the following sentence now starts "Under this correspondence" to avoid repeating the citation. |
| 10 | Imprecision | Yes. | **Applied, reworded:** "We assume that the label set has at least $\lvert G\rvert$ elements, as it must for the hidden subgroup $H = 1$." |
| 11 | Style | Yes. | **Applied:** $\approx 2^{174.72}$, $\approx 2^{174.47}$ (two decimals kept) and the caption sentence. |
| 12 | Style | — | **Rejected** by owner instruction: keep every "AI-checked, pending human review" label. |

## Final text

### Abstract

```latex
Let $G$ be a finite $p$-group of nilpotency class $c < p$, given by the structure constants of its Lazard Lie algebra $\mathcal{L} \cong \Fp^m$, and let $f$ hide an arbitrary subgroup $H \le G$. Beyond class two, the known polynomial-arity method for aligning random central characters, the degree-by-degree elimination of Ivanyos and Santha, needs automorphisms that preserve $H$ and scale the centre, and such automorphisms need not exist: the eight-dimensional class-three Dixmier--Lister algebra has no positive grading over $\Fp$ for any $p > 3$. We do not grade $G$. Instead we query $f$ at $c$ distinct nonzero evaluations of the graded cover $\A = \bigoplus_{k=1}^c t^k\gamma_k(\mathcal{L})$. The resulting oracle hides a homogeneous subgroup of the cover, which every graded dilation preserves, although the oracle uses no knowledge of $H$; one evaluation is not enough. The Ivanyos--Santha descent then removes the grades $c,\dots,2$ exactly, branch by branch, and grade one retains all of $\log H$, which abelian Fourier sampling recovers. With their fixed-degree diagonal-equation solver as an imported theorem, the algorithm has bounded error and runs in time polynomial in $m$, $\log p$, the label width and $\log(1/\eps)$ for every fixed $c$, with an explicit query count. In the same oracle model, for $m \ge 2$, the classical randomized query complexity is $\Theta(p^{(m-1)/2})$, even for non-normal hidden subgroups of order $p$ when $\mathcal{L}$ is not abelian. Conditional extensions are described in an outlook. All proofs have been checked by AI sessions only and are pending human review.
```

### Informal sentence, Theorem 1.2, and the sentence after it

```latex
Informally: for each fixed class $c$, and assuming the imported Ivanyos--Santha solver (Theorem~\ref{thm:is-import}), the HSP in $p$-groups of class $c < p$ given by the structure constants of their Lazard Lie algebra can be solved with bounded error, for every hidden subgroup, by a quantum algorithm whose running time is polynomial in $\log|G| = m\log_2 p$, the label width and $\log(1/\eps)$, and whose query count is explicit.

\begin{theorem}[Main theorem]
\label{thm:main}
Fix an integer $c \ge 1$ and assume Theorem~\ref{thm:is-import}. There is a quantum algorithm with the following guarantee.
\begin{enumerate}[label=(\arabic*),leftmargin=2em]
  \item \emph{Input.} An instance of Definition~\ref{def:input-contract}: a prime $p > c$; the structure constants of a nilpotent Lie algebra $\mathcal{L} \cong \Fp^m$ with $\gamma_{c+1}(\mathcal{L}) = 0$, which define the group $G = (\mathcal{L},\ast)$; a rational $\eps \in (0,1)$; and an arbitrary subgroup $H \le G$, given either \textup{(a)} by a coherent oracle $U_f$ for a function $f : G \to \{0,1\}^w$ with $f(x) = f(y) \iff x^{-1}\ast y \in H$, or \textup{(b)} by fresh independent copies of $\rho_H$.
  \item \emph{Output.} With probability at least $1-\eps$, a basis of $\hh = \log H$, and hence generators of $H$.
  \item \emph{Query count.} Let $g_d = \dim_{\Fp}\gamma_d(\mathcal{L})$ and $\tau = \lceil\log_p(3/\eps)\rceil$. The algorithm makes at most
  \[
    Q_{\mathrm q} = c\,(m + \tau)\prod_{d=2}^{c} B_d(g_d)
  \]
  queries in case~\textup{(a)}, or uses at most $Q_{\mathrm q}$ copies of $\rho_H$ in case~\textup{(b)}, with $B_d$ as in~\eqref{eq:Bd}.
  \item \emph{Explicit bound.} The count satisfies
  \[
    Q_{\mathrm q} \;\le\; C_c\, c\,(m+\tau)\,(m+1)^{\sum_{d=2}^c d\lceil\log_2(d+1)\rceil},
    \qquad
    C_c = \prod_{d=2}^c d^{\,d(d-1)\lceil\log_2(d+1)\rceil/2}.
  \]
  \item \emph{Gates.} Besides the queries, it uses classical operations and $\poly_c(m,\log p,w,\log(1/\eps))$ gates from a fixed finite universal gate set that implements $X$, CNOT and Toffoli exactly (for example Clifford$+T$).
\end{enumerate}
No property of $H$, such as normality, is assumed, and the guarantee is bounded-error, not exact.
\end{theorem}

The algorithm is the procedure of Section~\ref{sec:proof-main}: it uses the evaluation points $1,\dots,c$ and Schedule~1 (Section~\ref{sec:schedule1}) with arity $M_d = B_d(g_d)$ at every grade $d = 2,\dots,c$. For fixed $c$ the count $Q_{\mathrm q}$ is polynomial in $m$, and it does not depend on $p$ once $p \ge 3/\eps$, since then $\tau = 1$.
```

Content check against the old statement: every hypothesis ($c \ge 1$, the import, $p > c$, $\gamma_{c+1} = 0$, rational $\eps \in (0,1)$, oracle or copies, $H$ arbitrary), the output and its probability, $Q_{\mathrm q}$ and its two cases, the displayed bound with $C_c$, the gate count and gate set, "no property of $H$" and "bounded-error, not exact" are all present. The only material moved out of the statement is the description of which algorithm achieves it (points $1,\dots,c$, Schedule 1), which is not part of the guarantee and now sits in the next sentence. $g_d$ is recalled; $B_d$ is pointed to `eq:Bd`.

### Remark 1.3 (first property)

```latex
it is total, returning the scalars $s_1,\dots,s_{M_d}$ of a nonzero solution of~\eqref{eq:sde-target} (not only their $d$-th powers; Remark~\ref{rem:is-import}(a)) for any $M_d$ label columns in $\Fp^{g_d}$ and every prime $p > c$;
```

### After Remark 1.3 (appended to the paragraph)

```latex
The descent is the degree-by-degree elimination of~\cite{IvanyosSantha2015}; the cover is what lets it apply to an arbitrary $H$ in an arbitrary Lazard group (Section~\ref{sec:related}).
```

### Remark 8.3(a) (EHK)

```latex
For every finite group, Ettinger, H{\o}yer and Knill give a quantum algorithm that determines $H$ with error at most $\eps$ from $O(\log^2|G| + \log(1/\eps))$ queries~\cite[Theorem~2]{EttingerHoyerKnill2004}, here $O(m^2\log^2 p + \log(1/\eps))$, and one with exponentially small error from $O(\log^4|G|)$ queries~\cite[Theorem~1]{EttingerHoyerKnill2004}; both use exponential-time processing.
% NEEDS HUMAN VERIFICATION: ... (see file)
```

### Outlook, "Smaller arities" (changed clauses)

```latex
a block-steered variant, available at the grades with $2 \le \kappa_d < p-1$ and using $J_d = \max(3,\kappa_d)$ blocks, needs $\lfloor(g_d+2)^2/4\rfloor+[g_d\text{ odd}]$ columns when $\kappa_d \in \{2,3\}$, and $g_d^2/(2(J_d-1))+O(g_d)$ in general, at primes large compared with $g_d^2$ and the number of nodes (at $\kappa_d = 1$, $g_d+1$ columns suffice by linear algebra, Lemma~\ref{lem:bezout});
...
at fixed class, with weight-doubling witness nodes at the grades with $2 \le \kappa_d < p-1$, and Schedule~1 or another public node of the full version at a grade with $\kappa_d = p-1$ (which occurs only for $p = c+1$ and $d = c$), it would give polynomial classical time at every prime $p > c$,
```

### Other edits (Findings 8–11)

- Section 3.4: "Every such $D$ maps $\mathcal{L}_{\mathrm{DL}}$ into $\gamma_2(\mathcal{L}_{\mathrm{DL}}) = \Span(e_5,\dots,e_8)$, hence, by the derivation rule $D[x,y] = [Dx,y] + [x,Dy]$, maps $\gamma_2(\mathcal{L}_{\mathrm{DL}})$ into $\gamma_3(\mathcal{L}_{\mathrm{DL}}) = \Span(e_7,e_8)$ and $\gamma_3(\mathcal{L}_{\mathrm{DL}})$ into $\gamma_4(\mathcal{L}_{\mathrm{DL}}) = 0$, so $D^3 = 0$ and every derivation is nilpotent."
- Section 2: "We call a finite $p$-group of nilpotency class $c < p$ a \emph{Lazard $p$-group}; by the Lazard correspondence~\cite{Lazard1954,Khukhro1998}, every such group is isomorphic to $(\mathcal{L},\ast)$ for its Lazard Lie algebra $\mathcal{L}$. Under this correspondence, the subgroups ..."
- Section 8: "We assume that the label set has at least $|G|$ elements, as it must for the hidden subgroup $H = 1$."
- Table 1: class-9 row `$\approx 2^{174.72}$ & $\approx 2^{174.47}$`; caption adds "For the last row, the two threshold columns give the approximate size of the threshold rather than a prime."; caption "where $\tau = 1$".

## Companion counterparts

For the integrator of `docs/papers/rees-hsp/main.tex` (not applied here; line numbers are as of 5 November 2026, before the ongoing restructuring, so locate by text).

1. **Main theorem layout** (`thm:main`, "Proposed explicit-Lie theorem"). The companion uses $Q$ (not $Q_{\mathrm q}$) and puts the explicit bound in a display after the theorem. Replace the theorem body by:

```latex
Fix an integer $c \ge 1$ and assume Theorem~\ref{thm:is-import}. There is a quantum algorithm with the following guarantee.
\begin{enumerate}[label=(\arabic*),leftmargin=2em]
  \item \emph{Input.} An instance of Definition~\ref{def:input-contract}: a prime $p > c$; the structure constants of a nilpotent Lie algebra $\mathcal{L} \cong \Fp^m$ with $\gamma_{c+1}(\mathcal{L}) = 0$, which define the group $G = (\mathcal{L},\ast)$; a rational $\eps \in (0,1)$; and an arbitrary subgroup $H \le G$, given either \textup{(a)} by a coherent oracle $U_f$ for a function $f : G \to \{0,1\}^w$ with $f(x) = f(y) \iff x^{-1}\ast y \in H$, or \textup{(b)} by fresh independent copies of $\rho_H$.
  \item \emph{Output.} With probability at least $1-\eps$, a basis of $\hh = \log H$, and hence generators of $H$.
  \item \emph{Query count.} Let $g_d = \dim_{\Fp}\gamma_d(\mathcal{L})$ and $\tau = \lceil\log_p(3/\eps)\rceil$. The algorithm makes at most
  \[
    Q = c\,(m + \tau)\prod_{d=2}^{c} B_d(g_d)
  \]
  queries in case~\textup{(a)}, or uses at most $Q$ copies of $\rho_H$ in case~\textup{(b)}, with $B_d$ as in Theorem~\ref{thm:is-import}.
  \item \emph{Explicit bound.} The count satisfies
  \[
    Q \;\le\; C_c\, c\,(m+\tau)\,(m+1)^{\sum_{d=2}^c d\lceil\log_2(d+1)\rceil},
    \qquad
    C_c = \prod_{d=2}^c d^{\,d(d-1)\lceil\log_2(d+1)\rceil/2}.
  \]
  \item \emph{Gates.} Besides the queries, it uses classical operations and $\poly_c(m,\log p,w,\log(1/\eps))$ gates from a fixed finite universal gate set that implements $X$, $\mathrm{CNOT}$ and Toffoli exactly (for example Clifford$+T$).
\end{enumerate}
No property of $H$, such as normality, is assumed, and the guarantee is bounded-error, not exact.
```

   and put right after the theorem: "The algorithm uses the evaluation points $1,\dots,c$ and Schedule~1 of Section~\ref{sec:sde} with arity $M_d = B_d(g_d)$ at every grade $d = 2,\dots,c$. For fixed $c$ the count $Q$ is polynomial in $m$, and it does not depend on $p$ once $p \ge 3/\eps$, since then $\tau = 1$." The later sentence "Explicitly, with Schedule~1 the procedure makes at most [display] oracle queries ..., where $C_c = \dots$ depends only on $c$." then duplicates item (4); shorten it to "The running time is polynomial in $Q$ and in $m$, $\log p$, the label width and $\log(1/\eps)$." and keep the rest of that paragraph. In `rem:main-solver`, apply the Finding 6 text above (first property). Optionally add the informal sentence before the theorem (core text above, with Theorem~\ref{thm:is-import}).

2. **Surplus $t \to \tau$.** The companion's notation table (line ~282) already declares that $t$ and $\tau$ are reused, and its appendices use $\tau_d$ for abort targets next to the surplus (rule (R1) of `appendix-free-coordinate.tex`: "Let $t = \lceil\log_p(3/\eps)\rceil$ and $S = m + t$ ... $\tau_d = \eps/(9(c-1)Sn_d)$"). Recommendation: rename the surplus to $\tau$ in the body of `main.tex` only, where it collides with the Rees $t$: the theorem (above), the proof item "Rank" (line ~591: "Take $m + \tau$ terminal samples with $\tau = \lceil \log_p(3/\eps)\rceil$. Then the rank failure probability is at most $1/((p-1)p^\tau) \le \eps/3$."), $N_{\mathrm{solver}} = (m+\tau)\dots$ and "$S = m+\tau$" (lines ~592–593), Proposition `prop:classical-query`(v) and its proof (line ~1281: "$\tau = \lceil\log_p(2/\eps)\rceil$", then every $2t+2$, $k+t$, $p^{-t}$, $m+t$, $(t+1)$ in that proof, as in the core), Table `tab:query-crossover` caption ("where $\tau = 1$") and the display at line ~1333. If the body's $\tau$ is used anywhere for an abort target, keep $t$ in the appendices and add a notation-table row "$\tau$ & sample surplus $\lceil\log_p(3/\eps)\rceil$ (written $t$ in the appendices) & Thm.~\ref{thm:main}". Check the BCH proof of `thm:uniform-compilation`(i) in `main.tex`: if its ODE parameter is $\tau$, rename it to $\xi$ as in the core. Grep `m+t`, `m + t`, `p^t`, `p^{-t}`, `t = \lceil` after the restructuring.

3. **Block-steered wording.** No change needed: `rem:combined-schedule` ("Block-steered option") and (R1) already state $J_d = \max(3,\kappa_d)$ and $2 \le \kappa_d < p-1$. If the restructured companion gains an Outlook-style summary, use the core's sentence above verbatim.

4. **Schedule 3 fixed-class sentence.** No change needed: `main.tex` line ~788 ("... and a grade with $\kappa_d = p-1$ uses the node of Remark~\ref{rem:fc-zero-sum-arity}(b) or Schedule~1 rather than the zero-sum node ...") and `rem:fc-witness-h3`(c) are already complete. Any new summary sentence should use the core's wording above.

5. **EHK** (`rem:query-separation`(a), line ~1337). Replace "Ettinger, H{\o}yer and Knill determine $H$ in any finite group with $O(\log^2|G| + \log(1/\eps))$ queries~\cite[Theorem~2]{EttingerHoyerKnill2004}, here $O(m^2\log^2 p + \log(1/\eps))$, but with exponential-time processing." by the core's sentence above, and add the same `% NEEDS HUMAN VERIFICATION` comment. Keep the companion's "Theorem~\ref{thm:main}, if correct, adds ..." in the next sentence.

6. **Smaller items with identical companion text.**
   - Finding 10, `main.tex` line ~1252: "The label set has at least $|G|$ elements." → "We assume that the label set has at least $|G|$ elements, as it must for the hidden subgroup $H = 1$."
   - Finding 8, `main.tex` line ~461: "Every such $D$ maps $\mathcal{L}_{\mathrm{DL}}$ into $[\mathcal{L}_{\mathrm{DL}},\mathcal{L}_{\mathrm{DL}}]$ and $[\mathcal{L}_{\mathrm{DL}},\mathcal{L}_{\mathrm{DL}}]$ into $\operatorname{span}(e_7,e_8)$, which it kills, so $D^3 = 0$." → "Every such $D$ maps $\mathcal{L}_{\mathrm{DL}}$ into $\gamma_2(\mathcal{L}_{\mathrm{DL}}) = \operatorname{span}(e_5,\dots,e_8)$, hence, by the derivation rule $D[x,y] = [Dx,y] + [x,Dy]$, maps $\gamma_2(\mathcal{L}_{\mathrm{DL}})$ into $\gamma_3(\mathcal{L}_{\mathrm{DL}}) = \operatorname{span}(e_7,e_8)$ and $\gamma_3(\mathcal{L}_{\mathrm{DL}})$ into $\gamma_4(\mathcal{L}_{\mathrm{DL}}) = 0$, so $D^3 = 0$."
   - Finding 11, `main.tex` line ~1323: `$2^{174.72}$ & $2^{174.47}$` → `$\approx 2^{174.72}$ & $\approx 2^{174.47}$`, plus the caption sentence above.
   - Finding 9: add the core's "Lazard $p$-group" definition sentence to the companion's preliminaries.

## Not done

Nothing committed. Companion counterparts not applied (another agent owns `main.tex`). The EHK theorem numbers in the IPL version and every AI reading above still need a human.
