> Owner chose a readable variant (2026-11-05); the abstract-solver draft was not applied; see I230.

# OD3 draft: main theorem with an abstract arity A_d (not applied)

Owner decision OD3. Source: `2026-11-05-rees-referee-17-core.md`, Finding 2 and Recommendation 1;
`2026-11-05-rees-referee-17-applied.md`, "Owner decisions" item 1. Prepared 5 November 2026 by an
AI session. Status: draft for owner approval; `docs/papers/rees-hsp/core/main-core.tex` is untouched.
All results remain AI-checked, pending human review.

Files:

- `2026-11-05-rees-od3-draft/main-core.tex`: the edited copy.
- `2026-11-05-rees-od3-draft/od3.diff`: `diff -u` against `core/main-core.tex` (54 insertions, 30 deletions).
- `2026-11-05-rees-od3-draft/references.bib`, `numbers.tex`: identical copies, needed for the build. Neither changed.

## Which theorem

The brief says "Theorem 5.1". In the core paper Theorem 5.1 is the *imported* Ivanyos–Santha
statement (`thm:is-import`). The theorem the referee asks to restate is the main theorem
(`thm:main`). It was Theorem 1.2 and is Theorem 1.3 in the draft, because a definition now
comes before it. The draft restates `thm:main` and leaves Theorem 5.1 word for word as it was.
Theorem 5.1 is now used only by the new corollary.

## What changed

1. **New Definition 1.2 (`def:sde-solver`, "Per-grade solver").** A degree-$d$ solver of arity
   $A_d$ is a function $A_d(p,a)$, defined for primes $p>c$ and $a\ge0$, together with a
   deterministic classical algorithm $\mathcal S_d$ that satisfies hypotheses (i)–(iv) below.
2. **Theorem 1.3 (`thm:main`) restated.** It assumes a solver $\mathcal S_d$ of arity $A_d$ for each
   $2\le d\le c$, in place of "assume Theorem 5.1". It uses $M_d=A_d(p,g_d)$, and its bound is
   $Q_q=c(m+t)\prod_d A_d(p,g_d)\le C\,c(m+t)(m+1)^{\sum_d e_d}$, where $C=\prod_d C_d$. The rest of
   the statement is unchanged.
3. **New Corollary 1.4 (`cor:main-is`).** Its title reads "With the Ivanyos–Santha solver; rests on an
   AI-only reading of [IvanyosSantha2015], pending human confirmation". Assuming Theorem 5.1, it
   shows that Schedule 1 is a degree-$d$ solver of arity $B_d$, with
   $C_d=d^{d(d-1)\lceil\log_2(d+1)\rceil/2}$ and $e_d=d\lceil\log_2(d+1)\rceil$. It carries the old
   displayed bound with $C_c$. The definition `eq:Bd` of $B_d$ moved to sit just before it.
4. **Paragraph after the corollary.** It says that Theorem 1.3 does not depend on the reading of
   the source and Corollary 1.4 does, and it points to Remarks 5.2(e) and 5.3. The exponent
   $\ReesClassNineQueryExp$ (145) at $c=9$ is now attributed to the corollary. The list of
   imported ingredients is split: Theorem 1.3 imports only Lazard and the QFT compilation, and the
   corollary also imports Theorem 5.1 and van de Woestijne.
5. **Abstract.** The Ivanyos–Santha sentence now reads: "given, at each grade, a deterministic
   polynomial-time solver … polynomial arity …; the Ivanyos–Santha algorithm is such a solver, on an
   AI reading … that still needs human confirmation, and it makes the query count explicit."
6. **Introduction.**
   - The "Classical query complexity" paragraph now cites the corollary for the explicit separation.
   - The Related Work sentence on Imran–Ivanyos now reads "Theorem 1.3, with the solvers of
     Corollary 1.4".
   - Proof overview (c) now reads "per-grade solver at arity $A_d(p,g_d)$; Ivanyos–Santha at $B_d(g_d)$ (Cor. 1.4)".
   - The Organization paragraph now says Section 7 proves the theorem and the corollary.
7. **Section 5.**
   - The intro says the main theorem takes the solver as a hypothesis.
   - Remark 5.2(d) is about the determinism of the abstract solvers.
   - Remark 5.3 ends: "$B_d$, and with it Corollary 1.4, its query count and the exponent 145, rest
     on this AI-only reading … Theorem 1.3, stated for an abstract arity $A_d$, does not."
   - The Schedule 1 paragraph is rewritten as the definition of the instantiated solver, given
     $M=B_d(a)$ columns. It also gains one sentence: by Lemma 5.4, solvers of degree $\kappa$ for
     primes with $\kappa\mid p-1$, one for each divisor $\kappa\ge2$ of $d$, give a solver in the
     sense of Definition 1.2 with $A_d(p,a)=A'_{\kappa_d}(a)$, where $A'_1(a)=a+1$. This covers the
     referee's form of the hypothesis, which assumes only $d\mid p-1$.
8. **Section 7.**
   - "The procedure", "Correctness", "Approximation", "Query count" and "Running time" now use
     $A_d$, $\mathcal S_d$ and Definition 1.2 (i)–(iv) instead of $B_d$, Theorem 5.1 and Lemma 5.4.
   - The old display $B_d(g_d)\le\dots$ is replaced by a one-line use of (iii).
   - A new paragraph, **Proof of Corollary 1.4**, checks (i)–(iv) for Schedule 1 and computes the
     exponent $1+\sum_{d=2}^9 d\lceil\log_2(d+1)\rceil=145$.
9. **Remark 7.1 (what the proof uses).** It now says the proof uses "the solvers $\mathcal S_d$ only
   through their guarantee on arbitrary columns".
10. **Table 1 caption.** It now says "$Q_q$ is the count of Corollary 1.4, that is, of Theorem 1.3 with
    the Ivanyos–Santha arity $B_d$; like that corollary, these values rest on an AI-only reading …
    that needs human confirmation." The table numbers are unchanged, because they are
    $c(m+t)\prod B_d(g_d)$ (Heisenberg: $8\cdot64=2^9$, which checks).
11. **Remark 8.3 (query separation).** The general theorem gives $Q_q\le C\,c\,(m+1)^{1+\sum e_d}$
    uniformly in $p$ once $t=1$. "Independent of $p$" and the explicit exponent are now attributed
    to the corollary.
12. **Open problems.** The exponent of $m$ is set by the solver arities, and it grows like
    $c^2\log c$ in the corollary.

Unchanged:

- Theorem 5.1, Remarks 5.2(a)–(c), (e), the first part of Remark 5.3, Lemma 5.4, Remark 5.5, and
  the Heisenberg example ("Schedule 1 allots $B_2(1)=64$").
- The Outlook. Its uses of "Schedule 1", 145 and 143 still refer to the instantiation and stay correct.
- The appendix.
- Every "AI-checked, pending human review" label (26 before and after) and both
  `NEEDS HUMAN VERIFICATION` comments. "AI-only" now occurs 6 times instead of 3.

## Hypotheses on A_d and why each is needed

I checked every use of $B_d$, Theorem 5.1 and Schedule 1 in the old proof, grep-listed in the diff.
The proof needs the following properties and nothing else.

| Hypothesis in Def. 1.2 | Where the old proof used the corresponding property of $B_d$ / Theorem 5.1 |
|---|---|
| (i) Totality: for every prime $p>c$ and every label tuple with exactly $M=A_d(p,a)$ columns, the solver returns field elements $s_i$, not all zero. | Proposition 4.4 needs a nonzero solution for every positive-probability tuple. "No solver failure to budget" and the fixed $N_{\rm QFT}$ allocation need the solver to be total. Lemma 6.2's "every implemented step is a channel" needs it defined on every input. Returning the $s_i$ themselves, not $s_i^d$, is needed because $\delta_{s_i}$ is applied (old Remark 5.2(a)). |
| Deterministic algorithm | The witness must depend only on the labels and the public data $(p,d,g_d)$ (Remark 7.1), and the error budget has no solver share. Remark 5.2(d) still notes that Las Vegas would do. |
| (ii) Time $\mathrm{poly}_{d,c}(M,\log p)$ | The running-time paragraph. |
| (iii) $A_d(p,a)\le C_d(a+1)^{e_d}$, uniformly in $p$ | Several places need $M_d$, $P$, the number of merges and $N_{\rm QFT}$ to be polynomial in $m$: the running time, $\log N_{\rm QFT}=O_c(\log m+\log t)$, the explicit $Q_q$ bound with $g_d\le m$, and the query separation, which needs a bound uniform in $p$. This polynomial majorant also replaces monotonicity in $a$, which the proof does not otherwise use. |
| (iv) $A_d(p,a)$ computable in $\mathrm{poly}(a,\log p)$ | The algorithm must compute $M_d$ to size the tree and fix $N_{\rm QFT}$ and $\eta$ before the run ("arities public and fixed"). |
| Codomain: positive integers | A nonzero output needs $M\ge1$. Any valid solver satisfies this automatically. |

Monotonicity of $B_d$ in $d$ ($B_\kappa\le B_d$) is **not** a hypothesis on $A_d$. It was needed
only because Schedule 1 reduces to $\kappa_d=\gcd(d,p-1)$. In the draft, Definition 1.2 asks for a
solver at every prime $p>c$, and the $\kappa$ reduction, with its monotonicity, moved into the proof
of Corollary 1.4. I let $A_d$ depend on $p$ for two reasons: the reduction then works for arbitrary
solvers, giving $A_d(p,a)=A'_{\kappa_d}(a)$ (Section 5, last sentence), and $p$-dependent rules
such as Schedule 2 and the per-grade rule fit the definition. If the owner prefers the referee's
$A_d:\mathbb N\to\mathbb N$, drop the argument $p$. Remark 8.3 then gets back "independent of $p$"
for the general theorem. Nothing else changes.

The referee's proposed statement replaces $B_d$ by $A_d$ with "$d\mid p-1$" and keeps the rest
unchanged. That version silently needs $A_{\kappa}\le A_d$ for $\kappa\mid d$, and $A_d(a)\ge a+1$,
because Schedule 1 runs at degree $\kappa_d$ on the first $A_{\kappa_d}$ columns. The draft avoids
both hypotheses.

## Build

Scratch directory `/private/tmp/claude-501/-Users-jaspersands-Developer-qsearch/6a6cfdd7-c9d4-4169-9805-7e18625bbdd7/scratchpad/build_od3`,
built with `PATH=/Library/TeX/texbin:$PATH latexmk -g -pdf -interaction=nonstopmode main-core.tex`.

- Exit 0, **29 pages**. The current core builds to 28 pages, which I rebuilt in `build_od3_orig` to check.
- 0 Overfull and 0 Underfull boxes.
- No undefined references or citations, no multiply defined labels, no "Float too large".
- BibTeX: 0 warnings.
- The new LaTeX contains none of `\mathsf`, `\mathrel`, `\begingroup`, `\aa` or `\ni`.
- `make_numbers.py` was not run, and the macros are unchanged.

New numbering: Definition 1.2 (`def:sde-solver`), Theorem 1.3 (`thm:main`), Corollary 1.4
(`cor:main-is`). Theorem 5.1 and Remarks 5.2 and 5.3 keep their numbers.

## How to apply (after owner approval)

1. `cp research/audits/reviews/2026-11-05-rees-od3-draft/main-core.tex docs/papers/rees-hsp/core/main-core.tex`.
   `references.bib` and `numbers.tex` need no copy.
2. Optionally delete the two-line "OD3 DRAFT" comment at the top (lines 7–8).
3. Rebuild the core and recheck the counts above.
4. The full version `../main.tex` has the same main theorem. Port the same change there, or record
   the core and full versions as out of sync in the integration log. Not done here.
5. In `2026-11-05-rees-referee-17-applied.md`, mark Owner decision 1 (F2) as resolved by option (b).
   Human confirmation of the arXiv:1503.09016v2 reading is still needed for Corollary 1.4, and the
   hedges stay in place.

## Companion port (not applied)

Prepared 5 November 2026 by an AI session. This section ports the change to the full version
`docs/papers/rees-hsp/main.tex`, which is how-to-apply step 4 above. That file is untouched.
All results remain AI-checked, pending human review.

Files are in `2026-11-05-rees-od3-draft/companion/`:

- `main.tex` is the edited copy. `od3-main.diff` is `diff -u` against `docs/papers/rees-hsp/main.tex`
  (80 insertions, 40 deletions).
- The six `appendix-*.tex` files, `main-full-draft.tex`, `numbers.tex` and `references.bib` are
  identical copies, needed for the build. They have no diff because none of them changed.

### What changed in main.tex

The content shared with the core uses the core draft's wording. Where the two papers differ, the
companion keeps its own conventions: the symbol $Q$ in place of $Q_{\mathrm q}$, the inline
$\lceil\log_p(3/\eps)\rceil$ (because $t$ is the Rees variable there), the "Proposed explicit-Lie
theorem" title, and its Remark 4.5(b) in place of the core's Lemma 5.4.

1. **Definition 1.2 (`def:sde-solver`)**, identical to the core's. **Theorem 1.3 (`thm:main`)** is
   restated with $\mathcal S_d$, $M_d=A_d(p,g_d)$, and the bound $Q\le C\,c(m+\lceil\log_p(3/\eps)\rceil)(m+1)^{\sum e_d}$
   with $C=\prod_d C_d$, which is now inside the theorem. **Corollary 1.4 (`cor:main-is`)** has the
   core's title and hedge. It states the Schedule 1 count and the $C_c$ bound, which used to be
   displayed after the theorem. The $B_d$ display now comes just before the corollary.
2. **The paragraph after the corollary.** Theorem 1.3 is independent of the reading of the source,
   and Corollary 1.4 is not (Remark 4.5(c),(e)). The exponent 145 is attributed to the corollary. The
   imported ingredients are split: the theorem imports Lazard, the QFT compilation and Solovay–Kitaev,
   and the corollary adds Theorem 4.4 and van de Woestijne. The classical-separation sentence now has
   the core's wording.
3. **Abstract.** It has the core's two sentences: one about the abstract solver, and one saying
   Ivanyos–Santha "is such a solver, on an AI reading … that still needs human confirmation". Related
   work: both "if Theorem … is correct" sentences now read "with the solvers of Corollary 1.4".
   Table 1 caption: the fixed-class row is the corollary. Contributions (1) and (3) and the
   Organization paragraph are updated. Two notation rows are new: $A_d,\mathcal S_d$, and
   $C_d,e_d$. The second warns that $C_d$ is not the absolute constants $C_1,C_2,C_3$ of
   Remark 4.6. That clash already existed, in Remark 4.6 and Appendix E.
4. **Section 4.2.** The error-split bullets and the instrument count refer to solvers as in
   Definition 1.2, "in particular Schedule 1". The **Proof of Theorem 1.3** uses $A_d$ and
   $\mathcal S_d$, with (i) for correctness, (iii) for the bound, (ii) for time and (iv) for
   computing $M_d$. A new **Proof of Corollary 1.4** follows the core's, with the conversion of
   Remark 4.5(b) in place of the core's Lemma 5.4, and ends with the exponent 145.
5. **"Steps behind Theorem 1.3".** The paragraph keeps the clause "at every grade where Schedule 1
   is called, Theorem 4.4 …". It gains a convention sentence: wherever the paper or its appendices
   use Theorem 1.3 with the arities of Schedule 1, of the combined rule, or of another rule that
   calls Schedule 1, they use it through Corollary 1.4 and keep Theorem 4.4 as a hypothesis, as
   before. Because of this sentence, the about 30 references in the appendices, including
   Theorem 7.2 (`thm:bb-envelope`), Corollary 6.2 and the subspace core, keep their meaning and
   need no edit.
6. **Remark 4.5.** Part (c) gets the core's closing sentences: $B_d$, Corollary 1.4, its count and
   145 rest on the AI-only reading, and Theorem 1.3 does not. Part (d) is reworded for the solvers
   of Definition 1.2. The Schedule 1 paragraph gets two additions: Schedule 1 is the solver of
   Corollary 1.4, and the core's reduction sentence ($A_d(p,a)=A'_{\kappa_d}(a)$, $A'_1(a)=a+1$).
7. **New Remark 4.18 (`rem:schedules-abstract`).** It says which schedules fit Definition 1.2. None
   of them is restructured.
   - (a) Schedule 1 fits, given Theorem 4.4. The linear solver fits at the primes with $\kappa_d=1$.
     Linear or Schedule 1 at degree $\kappa_d$ is a solver of arity at most $B_d$; it is the combined
     rule without Schedule 2.
   - (b) Schedule 2 and the triangular solver are Las Vegas, not deterministic. The combined rule is
     therefore covered by the solver share of the error budget (Remark 4.5(d)), not by
     Definition 1.2 as stated, and it stays conditional on Theorem 4.7(ii).
   - (c) Schedule 3 (both samplers, parts (i)–(iv)), the weight-doubling nodes and the mixed
     uniform-kernel nodes do not fit. They need the i.i.d. label law, abort on some banks, and in
     parts (ii) and (iv) restart whole trees, so they keep their own theorem and error splits. The
     zero-sum node is total and deterministic, but its search is exponential in $g_d$, so it fails (ii).
   - (d) The coherent receiver is stated at the arities of Corollary 1.4 and extends to
     Definition 1.2 solvers once a step bound is given.
8. **References that meant the explicit count now point to Corollary 1.4.** These are the "query
   counts of" sentences in Remarks 4.11 and 4.13, the circuit-backend scope text, the
   coherent receiver title and the text after it, the scalar-flag remark after Corollary 6.1, the
   black-box Theorem 7.2(i), Remark 8.5 (query separation) and the Table 8 caption. Remark 8.5
   first states the general bound $C\,c(m+t)(m+1)^{\sum e_d}$, then the $p$-independent Schedule 1
   count, with the AI-only hedge.

Not changed: Theorem 4.4 itself, Remark 4.6, Theorems 4.7 and 4.16 (`thm:free-coordinate`), the
combined rule, the appendices, and the research-status box. The status box could gain a sentence if
OD3 is applied. Every "AI-checked, pending human review" label is kept: there are 90 before and
after. Both `NEEDS HUMAN VERIFICATION` comments are kept: there are 13 of them before and after.
"AI-only" now occurs 25 times instead of 17. The new LaTeX contains none of `\mathsf`, `\mathrel`,
`\begingroup`, `\aa` or `\ni`.

### Build

Scratch directory `/private/tmp/claude-501/-Users-jaspersands-Developer-qsearch/6a6cfdd7-c9d4-4169-9805-7e18625bbdd7/scratchpad/build_od3c`,
built with `PATH=/Library/TeX/texbin:$PATH nice -n 19 latexmk -g -pdf -interaction=nonstopmode main.tex`.

- Exit 0, **179 pages**. The current companion builds to 177 pages; I rebuilt it in `build_od3c_orig` to check.
- 0 Overfull boxes. There are 3 Underfull boxes, all in the bibliography, and the baseline has the same 3.
- No undefined references or citations, no multiply defined labels, no "Float too large".
- BibTeX: 0 warnings.
- New numbering: Definition 1.2, Theorem 1.3 (`thm:main`), Corollary 1.4, Remark 4.18. Everything
  after them in Section 1 moves down by two. Section 4 numbering is unchanged, because the new
  remark is the last item in that section.
- Numbers test. `tests/tools/test_rees_paper_numbers.py` cannot be pointed at another path, since
  `PAPER` is hard-coded, so I did not run it against the draft. I called the same check function,
  `check_tex_uses(defined, tex_path)` from `make_numbers.py`, with the draft path: it reports no
  undefined macros. `numbers.tex` is byte-identical. `make_numbers.py` was not run as a script.

### How to apply (after owner approval, together with the core)

1. `cp research/audits/reviews/2026-11-05-rees-od3-draft/companion/main.tex docs/papers/rees-hsp/main.tex`,
   or `patch docs/papers/rees-hsp/main.tex research/audits/reviews/2026-11-05-rees-od3-draft/companion/od3-main.diff`
   from the repository root. Naming the target explicitly avoids any ambiguity, since both paths in the diff header exist. A dry run in scratch applied cleanly.
   No appendix, `numbers.tex` or `references.bib` copy is needed.
2. Optionally delete the two-line "OD3 DRAFT" comment (lines 2–3), and add one sentence on OD3 to
   the research-status box.
3. Rebuild and recheck the counts above. Run `pytest tests/tools/test_rees_paper_numbers.py`
   against the live paper.
4. Record the change in the integration log, for both the core and the companion.
