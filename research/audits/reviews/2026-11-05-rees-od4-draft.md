# OD4 draft: Outlook cut to about half a page (not applied)

Owner decision OD4. Source: `2026-11-05-rees-referee-17-core.md`, Finding 18 (Outlook length,
proposed new opening) and Recommendation 3; `2026-11-05-rees-referee-17-applied.md`, "Owner
decisions" item 2. Prepared 5 November 2026 by an AI session. Status: draft for owner approval;
`docs/papers/rees-hsp/core/main-core.tex` is untouched. All results remain AI-checked, pending
human review.

Files:

- `2026-11-05-rees-od4-draft/main-core.tex`: the edited copy (based on the current core, not on OD3).
- `2026-11-05-rees-od4-draft/od4.diff`: `diff -u` against `core/main-core.tex`. One hunk, inside
  Section 9 only; 5 paragraph lines in, 13 out.
- `2026-11-05-rees-od4-draft/od4-on-od3.diff`: the same cut, rebased onto the OD3 draft file (see
  "Interaction with OD3").
- `2026-11-05-rees-od4-draft/references.bib`, `numbers.tex`: identical copies, needed for the build.

## What changed

Section 9 (Outlook) went from about 2.7 pages (p. 21 to the middle of p. 24) to about 0.6 page
(pp. 21–22, about 28 lines of text). The section title and `\label{sec:outlook}` are kept, so the
abstract, the Section 1 pointer to the black-box composition, the roadmap and Appendix A still
resolve. Nothing outside Section 9 changed.

New structure:

1. **Opening (scope statement).** Nothing in the section is claimed. The results of the paper are
   Theorem `thm:main` and Proposition `prop:classical-query`, with the status of Section 1.6. Every
   item is conditional or *argued* (not proved in the full version either). All items are
   AI-checked, pending human review, and their derivations are in the full version. This is the
   referee's proposed opening, reworded.
2. **Smaller arities.** Schedule 2: the bound $(g_d+1)((\kappa_d-1)g_d+1)$ for
   $p\ge16\kappa_d^{2\kappa_d+2}$, and the triangular variant $(g_d+1)(g_d+2)/2$ outside finitely
   many primes. The per-grade rule lowers the exponent only from 145 to 143 at $c=9$. Schedule 3
   uses the label law; it gives the derived-dimension time bound $2^{O(r\log(r+2))}\cdot\poly$
   for the independent supply only. Status tag kept.
3. **Black-box nilpotent groups.** The composition (pullback, ring-to-field recursion, Imran–Ivanyos
   for $p\le c$), with its full list of conditions. Tag: "AI-checked, pending human review; not
   claimed here". Kept because Section 1 points to it.
4. **Further items.** One sentence each: codimension and subspace sources (conditional), the
   early-measurement lower bound (argued, and not a bound for this procedure), no known
   application, and the classical filters. One status tag.
5. **Open problems, numbered (1)–(5).** (1) The $O(a)$-column solver, with the $O(a^2)$
   triangular bound and the conditional cryptographic hardness at arity $a+2$ (tag kept). (2) An
   exact algorithm. (3) A bound uniform in $c$. (4) The black-box case without the conditions.
   (5) A natural application that passes the classical filters. Items (1)–(4) were in the old
   text; (5) restates the old Applications paragraph as a problem.

Cut (all of it remains in the companion, `docs/papers/rees-hsp/main.tex` and its appendices):

- Schedule 2 details: the construction steps, the exceptional sets $E_2(\kappa)$ ($\kappa\le9$),
  the $6\kappa^\kappa+1$ threshold and its argued $O(\kappa^\kappa)$ and $\kappa^\kappa/2$
  claims, the randomized $o(a^2)$ solvers, the tower and chain refinements.
- Schedule 3 details: $4u$ columns, $p\ge16u^2$, the free-coordinate arity formula, the
  weight-doubling nodes, the non-adaptive lower bound, the SIS/worst-case lattice reduction, and
  the zero-sum node at $p=c+1$.
- The Ivanyos–Magniez–Santha route for the derived-dimension bound, and the filiform
  codimension example with its $2^{O(k\log(k+2))}$ bound.
- Prime-power details ($\Omega_1(G)$, $b$ calls, the torsion rank $R$), $E_W(c)$, $E_W(9)=143$,
  and the $E_1(c)$ formula.
- The subspace-source construction (exterior powers, streaming antisymmetrization, zero-moment
  design), its parameters, and the argued spectral-flag extension.
- The details of the early-measurement interface: the $\Omega(p^{(c-1)(c-2)/2})$ bound and the
  exact controls at $c=3,4$.
- The Applications details: the matrix-tuple stabilizer, Luks, the black-box reductions to linear
  algebra, and the "fourth search" result on circuit polynomials (proved there; possibly known).

Status labels. Section 9 had 19 occurrences of "AI-checked, pending human review"; the draft has
5. Every claim that stays has a tag of its own, and the opening covers the whole section. Each tag
removed went with the claim it covered. No `NEEDS HUMAN VERIFICATION` comment was in Section 9; the
two in the paper (lines 433 and 504) are untouched. The Section 1.6 disclaimer and the `\date`
footnote are untouched.

References. Three keys were cited only in Section 9 and are no longer cited: `BeneWatts2026`,
`IvanyosMagniezSantha2001`, `Luks1992`. They drop out of the printed bibliography (29 to 26
entries). `references.bib` is unchanged, so the Appendix A claim that every entry appears in the
master file still holds.

## Build

Scratchpad `build_od4`, `PATH=/Library/TeX/texbin:$PATH latexmk -g -pdf -interaction=nonstopmode
main-core.tex`: exit 0, **26 pages** (the current core builds to 28 in `build_od4_base`). 0
Overfull, 0 Underfull, no undefined reference or citation, no "Float too large", no rerun
warning, BibTeX 0 warnings. The added lines use no `\mathsf`, `\mathrel`, `\begingroup`, `\aa` or
`\ni`. `make_numbers.py` was not run, and the only number macro used is `\ReesClassNineQueryExp`,
as before.

## Interaction with OD3

The two drafts are independent: each was made from the current core. **`od4.diff` does not apply
cleanly on top of the OD3 draft.** `patch --dry-run` on a scratch copy of
`2026-11-05-rees-od3-draft/main-core.tex` fails its one hunk, even with `-F3`. Both drafts rewrite
the "Open problems" paragraph: OD3 rewords its first sentence for the abstract arity. Applied to the
current core, `od4.diff` dry-runs cleanly.

`od4-on-od3.diff` is the same cut against the OD3 draft file. It has two OD3 wordings:

- Smaller arities: "lowers the exponent of $m$ in Corollary~\ref{cor:main-is} at $c=9$ only
  from 145 to 143";
- Open problem (1): "The exponent of $m$ in Theorem~\ref{thm:main} is set entirely by the
  arities of the diagonal-equation solvers, and in Corollary~\ref{cor:main-is} it grows like
  $c^2\log c$".

It applies cleanly to a scratch copy of the OD3 draft. The result builds with exit 0, **27 pages**
(OD3 alone: 29), 0 Overfull, no undefined reference or citation, and BibTeX 0 warnings. If OD4 goes
in first, OD3's hunk at the Open problems line will fail in turn; apply OD3 by hand there.

## How to apply (after owner approval)

- OD4 alone: `patch docs/papers/rees-hsp/core/main-core.tex < research/audits/reviews/2026-11-05-rees-od4-draft/od4.diff`
  (or copy `2026-11-05-rees-od4-draft/main-core.tex` over it if the core has not changed since).
- OD3 then OD4: apply OD3 first (its own instructions), then
  `patch docs/papers/rees-hsp/core/main-core.tex < research/audits/reviews/2026-11-05-rees-od4-draft/od4-on-od3.diff`.
- Then rebuild the core and recheck the counts above. The full version needs no change, because
  its Outlook material is the source of everything cut here. In
  `2026-11-05-rees-referee-17-applied.md`, mark owner decision 2 (F18) as resolved. Optional:
  F18's other half, a single disclaimer, would also remove the per-item status tags. This draft
  keeps them, because the owner asked to keep status labels.
