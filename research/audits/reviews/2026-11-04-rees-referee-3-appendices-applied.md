# Referee report 3 (appendices): fixes applied

Date: 2026-11-04. Report: `research/audits/reviews/2026-11-04-rees-referee-3-appendices.md`.
Files edited: `docs/papers/rees-hsp/appendix-schedule3.tex`,
`docs/papers/rees-hsp/appendix-free-coordinate.tex`, `docs/papers/rees-hsp/main.tex`.
No other file was edited. Backup of all `.tex` files before editing:
`/private/tmp/claude-501/-Users-jaspersands-Developer-qsearch/6a6cfdd7-c9d4-4169-9805-7e18625bbdd7/scratchpad/bak-i156/`.

The report gives no finding ids. The ids below are the report's subsection
(A.0 to B.11) and the position of the finding among the non-"fine" items there.
All 28 non-"fine" findings are listed (1 error, 5 gaps, 22 imprecisions, as in
the report's count).

Rerun checks: `class9_checks.py`, `part2_cap_precise.py` and `rc_thm_cap.py`
(with `/opt/anaconda3/bin/python -I`) reproduce their committed outputs byte
for byte.

| Id | Class | Result | File | Note |
|---|---|---|---|---|
| A.0-1 | imprecision | applied | appendix-schedule3.tex | Intro now says the *second* proof of Cor. `cor:fpt-r` needs uniformity in `c`; the main proof uses Thm. `free-coordinate`(iii). |
| A.0-2 | imprecision | applied with edits | appendix-schedule3.tex | Appended the sentence on what Sec. `app:s3-mixed` uses; also listed Rem. `rem:combined-schedule`, which that section uses and the replacement left out. |
| A.1-1 | imprecision | applied | appendix-schedule3.tex | Added "the theorem then applies when $p \ge 16u^2$". |
| A.3-1 | imprecision (harmless) | applied with edits | appendix-schedule3.tex | Lemma `s3-moment`(d) now shows $\le 2p^{a-1-M} \le 2p^{a-M}$; proof sentence changed to name the third inequality. Downstream uses unchanged. |
| A.3-2 | imprecision (harmless) | skipped | appendix-schedule3.tex | No replacement offered. Dropping $M > a$ would also mean changing Lemma `s3-node`(a), which cites it. Harmless as written. |
| A.9-1 | imprecision | applied with edits | appendix-schedule3.tex | Lemma `s3-hybrid` uses $\mathcal{S}_j$ (statement and proof), with "(called $S_j$ in Lemma `lem:hybrid`)", because main.tex keeps $S_j$. |
| A.10-1 | imprecision | applied with edits | appendix-schedule3.tex, appendix-free-coordinate.tex | $B \le 6 + (u-1)\lceil\log_2 4u\rceil$ in Prop. `s3-uniform`(b), checked against the proof's own computation. The same bound, quoted as $7+\dots$ in the proof of Prop. `fc-uniform`(a), is changed to $6+\dots$ to match. Source comments recording the earlier $\le 7$ check are left alone. |
| A.10-2 | imprecision | applied | appendix-schedule3.tex | "$2g_d \le 2m$ coordinate transforms each", matching Thm. `uniform-compilation`(iii) (a transform and its inverse per top coordinate). |
| A.11-1 | gap | applied | appendix-schedule3.tex | Prop. `mixed-schedule`: choices are from the public data $p$, $c$, $(g_{d'})$ only, never from $H$, labels or coins. This covers the Table `fcs-budget` instance, whose column-adding rule reads $n_d$. The proof never used the narrower hypothesis. |
| A.11-2 | gap | applied | appendix-schedule3.tex | (S2) item: each (S2) node runs Phase 0 of Thm. `app-s2-main` with its own coins. Confirmed that Phase 0 depends only on $(p,\kappa,k)$, and Rem. `rem:app-s2-four` explicitly allows reusing it, which would correlate tree aborts. See decision 2. |
| A.11-3 | imprecision | applied | appendix-schedule3.tex | Tree-abort range restricted to the four (S3) primes: $2^{-6.91}$ to $2^{-6.38}$. `class9_checks_out.txt` confirms: no (S3) node at 11 or 1031, and the extremes are at $2^{127}-1$ and 5281. |
| B.0-1 | imprecision | applied with edits | appendix-free-coordinate.tex | No replacement text given, so wrote it. Body list: added Thm. `is-import` (the arity $B_d$), Rem. `combined-schedule`, Prop. `triangular-sde` and $E_2(\kappa)$ of Prop. `decoupled-sde` (for Rem. `fc-tradeoff`(a)). Appendix list: added Lemma `s3-hybrid` and Rem. `s3-caveat`. |
| B.1-1 | imprecision | applied | appendix-free-coordinate.tex | Removed the stale "applied with $\beta = \alpha'$". |
| B.1-2 | imprecision | applied | appendix-free-coordinate.tex | "nondecreasing in $a$" ($q = 1$ at $\kappa = 1$). |
| B.1-3 | imprecision (notation) | applied with edits | appendix-free-coordinate.tex | Round cap renamed $R_{\mathrm{rd}}$ at its definition, in $F_r$, and in Lemma `fc-node`(c),(e). A parenthesis says it is Lemma `s3-root`'s $R$, renamed because $R$ is the echelon matrix. |
| B.4-1 | imprecision (notation) | applied | appendix-free-coordinate.tex | Lemma `fc-node`: $\omega_{\mathcal{X}}$ and $\mathcal{X}$ in the statement and in (d). |
| B.4-2 | imprecision | applied | main.tex | Thm. `free-coordinate` preamble: the label law and $\kappa_d < p-1$ are assumed at the free-coordinate sampler nodes only, and part (iii) uses other nodes at the remaining grades. |
| B.6-1 | imprecision | applied | main.tex | Thm. `free-coordinate`(iii): "With the explicit choice, the arity is ...". |
| B.6-2 | imprecision | applied | appendix-free-coordinate.tex | The combined-arity variant needs the Bezout lift of Rem. `is-import`(b), plus Thm. `power-sde`(ii) only at Schedule 2 grades. This matches Rem. `combined-schedule`, which already lists the Bezout lift as a condition. |
| B.6-3 | imprecision | applied | main.tex | "no Schedule 1 call at a reduced degree (the free-coordinate nodes use only the elementary identity (eq:s3-bezout))" replaces "no Bezout lift". |
| B.7-1 | gap (minor) | applied with edits | appendix-free-coordinate.tex | Applied the $t_{\mathrm{S1}}$ replacement in Prop. `fc-uniform`(b). Without further edits the next sentence would be false (it calls $t_{\mathrm{S1}}$ polynomial), so it now says: polynomial for Schedule 1, and $\le M_d\kappa_d^{2g_d}\poly$ for the zero-sum node, using $p = \kappa_d+1 \le \kappa_d^2$. One clause added to the proof. The stated $2^{O(\max_d g_d\log\kappa_d)}$ time is unchanged. |
| B.8-1 | error (minor, numerical) | applied | appendix-free-coordinate.tex | Part (ii) per-node cap: the largest value is at $p = 194522647344910884721$ ($2^{34.2786}$), and it is $2^{34.27}$ at 5281. Confirmed by rerunning `part2_cap_precise.py`. |
| B.8-2 | imprecision | applied with edits | appendix-free-coordinate.tex, main.tex | $2^{128}$ is now attributed to the mixed instance of Prop. `mixed-schedule`. The report's "about $2^{224}$ or more" for Thm. `random-column`(ii) is **false at $p = 105019$**: `rc_thm_cap_out.txt` gives $2^{193.9}$ there. The appendix therefore says "between $2^{193.9}$ and $2^{236.0}$ ... at the six primes of (b)". main.tex says "$2^{223.8}$ to $2^{236.0}$ ... at the four primes of that table with $p \ge 16u^2$" (5281, $2^{31}-1$, $2^{61}-1$, $2^{127}-1$). |
| B.9-1 | imprecision | applied | appendix-free-coordinate.tex | Added "(in particular, not on the outcomes of earlier trials)" in the proof of Prop. `rc-lower`. The main.tex statement is unchanged (the report did not ask). |
| B.10-1 | imprecision (notation) | applied with edits | appendix-free-coordinate.tex | Used the report's "sentence" option instead of renaming to $N_j$, because $N$ already names the sampler-node count (R2) and the witness counts. The sentence says level counts $n_j$ are used only for $j \ge 1$, and $n_0^{(j)}$ is always a threshold. |
| B.11-1 | gap | applied | appendix-free-coordinate.tex | Rem. `fc-tradeoff`(a): time is "given the contraction $(\alpha,\beta)$, whose cost depends only on $(p,\kappa)$ and is not counted here". Confirmed that Prop. `triangular-sde` takes $(\alpha,\beta)$ as input. |
| B.11-2 | gap (minor) | applied with edits | appendix-free-coordinate.tex | Early stop: "back-substitution from its realisation already gives a solution" (the proof of Prop. `triangular-sde` back-substitutes from $R$, so the realisation alone is not the solution). |
| B.11-3 | imprecision (notation) | applied with edits | appendix-free-coordinate.tex | The dimension $a-K$ is renamed $g'$ everywhere in (a). The coset generator keeps the name $g$. |

Counts: 16 applied, 11 applied with edits, 1 skipped.

## Build and test

- Build in
  `/private/tmp/claude-501/-Users-jaspersands-Developer-qsearch/6a6cfdd7-c9d4-4169-9805-7e18625bbdd7/scratchpad/build/`
  with `latexmk -pdf -interaction=nonstopmode main.tex`: exit 0, **129 pages**
  (the same as before). No `Overfull`, no `Float too large`, no undefined or
  multiply defined references. There are three `Underfull \hbox` lines, all in
  `main.bbl` (known).
- `/opt/anaconda3/bin/python -m pytest -q -p no:cacheprovider tests/tools/test_rees_paper_numbers.py`:
  2 passed.

## For the integrator

1. **B.8-2.** The report's replacement figure ("$2^{224}$ or more") is wrong at
   105019. Check the ranges used instead.
2. **A.11-2 against Rem. `rem:app-s2-four`.** That remark (appendix-schedule2.tex)
   still says Phase 0 can run once per $\kappa_d$ and be reused at every node.
   Under Prop. `mixed-schedule`, reuse would break the binomial restart bound
   as written. One fix is a clause in that remark. Another is to allow reuse
   and add the failure of a single shared Phase 0 to the error budget. Not
   edited here, because the report did not name that file.
3. **B.7-1 follow-on.** The proof of Cor. `cor:fpt-r`(i) in main.tex still
   describes $t_{\mathrm{S1}}$ as "the time of one Schedule 1 call". That is
   harmless, because $t_{\mathrm{S1}} = 0$ there, but it now differs from the
   new definition. Left unchanged.
4. **B.6-2 / B.6-3.** The paper lists the Bezout lift of Rem. `is-import`(b) as
   a condition (Rem. `combined-schedule`), yet the free-coordinate nodes use the
   same elementary identity (eq. `s3-bezout`) without a condition. Whether the
   lift should remain a listed condition anywhere is the owner's call. The edits
   keep the current treatment.
5. **B.11-1 notation.** In Rem. `fc-tradeoff`(a) the contraction $(\alpha,\beta)$
   of Prop. `triangular-sde` now sits in the same sentence as the bank bound
   $\beta(\cdot,\cdot;\cdot)$. It reads unambiguously, but could be renamed.
