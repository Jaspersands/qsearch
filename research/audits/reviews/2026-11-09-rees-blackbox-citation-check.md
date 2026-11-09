# 2026-11-09 Rees black-box corollary: citation check (AI only, pending human review)

Scope: the two `NEEDS HUMAN VERIFICATION` markers in
`research/audits/reviews/2026-11-08-rees-blackbox-corollary-draft.tex` (comment at line 24;
part (A)(c) at line 39), the Khukhro item in
`research/audits/reviews/2026-11-05-rees-cloud-batch-results.md` ("Lazard correspondence
Thm 10.13, BCH Lemma 9.15"), and the UT_n claim in part (A)(a). No file other than this
report was edited, and no git actions were taken.

Bib status: `Khukhro1998` is in both `docs/papers/rees-hsp/references.bib` (l.136) and
`docs/papers/rees-hsp/core/references.bib` (l.135; the task's `core/references.bib` is this
file). Its fields (Evgenii I. Khukhro, LMS LNS 246, CUP 1998, doi 10.1017/CBO9780511526008)
match Cambridge Core. Neither bib has a `CicaloDeGraafVaughanLee2012` entry. A proposed entry
is in item 2.

## Sources actually read

| Source | What was read | URL |
|---|---|---|
| Cambridge Core, Khukhro book | chapter-level table of contents with page ranges; Ch. 9 summary and first-page preview | https://www.cambridge.org/core/books/pautomorphisms-of-finite-pgroups/5718587EAEFE8AC3BC603D34B68218BE ; Ch. 9: .../bakerhausdorff-formula-and-nilpotent-powered-groups/1A29355943B913F77F8F0EF2B0DE1292 ; Ch. 10: .../correspondences-of-a-i-malcev-and-m-lazard/D169684342CF32080232CCA1C78F1221 |
| **Cicalò–de Graaf–Vaughan-Lee 2012 (CdGVL)**, the publisher's PDF (J. Algebra page headers 430–450) from the Trento repository, via the Wayback Machine (the live IRIS and ScienceDirect pages return 403) | full text, especially §§1, 2, 7, 9.2 | http://web.archive.org/web/20261010091534/https://iris.unitn.it/retrieve/e3835192-3015-72ef-e053-3705fe0ad821/lazard.pdf |
| Crossref and zbMATH (Zbl 1254.20032, review by A. Caranti) | metadata | https://api.crossref.org/works/10.1016/j.jalgebra.2011.11.031 ; https://zbmath.org/?q=an:1254.20032 |
| V. Naik, *Lazard correspondence up to isoclinism*, PhD thesis, Chicago 2013 | every citation of Khukhro | https://files.vipulnaik.com/thesis/thesis.pdf |
| Díaz Ramos, Garaialde Ocaña, González-Sánchez, arXiv 1612.06584v1 | proof of their Thm 2.3 | https://arxiv.org/abs/1612.06584 |
| O'Brien–Voll, "Enumerating classes and characters of p-groups" (authors' PDF) | §2 | https://www.math.auckland.ac.nz/~obrien/research/characters.pdf |
| Grochow–Qiao, arXiv 1907.00309v1 | Thm 6.4, Prop 6.5 and its proof sketch | https://arxiv.org/abs/1907.00309 |
| GAP package LieRing: manual §§1.3, 2.4 and source `gap/lazard.gi` | `PGroupToLieRing`, `LieRingToPGroup` | https://docs.gap-system.org/pkg/liering/doc/chap2.html ; https://github.com/gap-packages/liering/blob/master/gap/lazard.gi |

The Khukhro book text itself was **not** reachable: the Cambridge chapter PDFs are paywalled,
the Google Books API returned a quota error, and archive.org is lending-only. So every locator
below that is finer than a chapter comes from secondary sources. CdGVL is the strongest of
these, because its third author is a specialist and it cites Khukhro by number three times.

## 1. Khukhro, *p-Automorphisms of Finite p-Groups*

### Chapter facts (primary: Cambridge Core)
- Ch. 9, "The Baker–Hausdorff Formula and nilpotent ℚ-powered groups", pp. 101–112.
- Ch. 10, "The correspondences of A. I. Mal'cev and M. Lazard", pp. 113–129.
- The Ch. 9 summary says the chapter constructs free nilpotent groups and Lie ℚ-algebras inside
  associative ℚ-algebras and proves that the Baker–Hausdorff formula is a Lie polynomial. It says
  Ch. 10 applies this to the Mal'cev correspondence and to the Lazard correspondence for class ≤ p−1.

### Finer locators found in secondary sources

| Locator | Content attributed | Who cites it |
|---|---|---|
| §9.2 | the Hausdorff series / BCH formula exists and is a Lie element | Naik (thesis §6.3); O'Brien–Voll §2 |
| Thm 9.2, Thm 9.18, Cor 9.22 | free nilpotent group in 1+A; roots; free ℚ-powered group | Naik |
| Lemma 9.15 | "the explicit Baker–Campbell–Hausdorff formula", used for log(G^p) = p·log G | Díaz Ramos et al. only |
| §10.1 | Mal'cev correspondence; inverse BCH formulas | CdGVL p. 444 (Remark 7.1: "[15, §10.1]" for Mal'cev); Naik (inverse formulas) |
| **Lemma 10.7** | e^{x+y} and e^{[x,y]} are infinite products of group commutators in e^x, e^y with rational exponents (the first and second inverse BCH formulas) | **CdGVL p. 433, cited twice**; Naik |
| Thm 10.4 | the ℚ-root closure of F equals e^{ℚL} | Naik |
| Thm 10.13 (parts (b), (c), (d)) "and page 124" | properties of the correspondence: normal subgroups ↔ ideals (b), class preserved (d) | Díaz Ramos et al. only |
| Thm 10.19, Thm 10.20 (p. 122), Thm 10.22 | π-roots; π-powered hull; σ-root closure of F = e^{ℤ[σ⁻¹]L} for σ ⊇ {primes ≤ c} | Naik |
| **§10.2** | the inverse formulas defining Lie sum and bracket in a finite p-group of class c < p (the Lazard setting) | **CdGVL p. 434** |
| Example 10.24 | Lazard correspondence: p-groups of class c < p ↔ Lie rings of p-power order and class c < p | O'Brien–Voll |

### Verdicts

**1(a) "inverse Hausdorff formulas, \cite[Chapters~9--10]{Khukhro1998}" (draft l.24 marker
and proof of Cor. black-box): CONFIRMED as a range, loose as a pointer.**
The forward BCH formula is in Ch. 9 (§9.2). The inverse formulas are in Ch. 10: Lemma 10.7 in
§10.1 over ℚ, and their finite-p-group, class-below-p form in §10.2 (CdGVL pp. 433–434). The
denominator control the draft needs, exponents in ℤ[1/c!], is Thm 10.22 according to Naik, and
CdGVL p. 433 states the same fact for the BCH coefficients. So "Chapters 9–10" is correct, but
the inverse formulas themselves are in **Chapter 10**, not Chapter 9.
- Confirmed from two independent secondary sources (CdGVL; Naik) for Lemma 10.7. Confirmed from
  one (CdGVL) for §10.2. None of these were seen in the book.

**1(b) Lazard correspondence: Chapter 10 CONFIRMED (primary); §10.2 CONFIRMED (secondary,
CdGVL, and consistent with the 2026-11-04 report's "§10.2, p. 121"); "Theorem 10.13"
UNCONFIRMED and probably imprecise.**
- The batch item "Thm 10.13, BCH Lemma 9.15" traces to Díaz Ramos et al. (arXiv 1612.06584,
  proof of Thm 2.3). They cite Lazard as "Theorem 10.13 and page 124".
- Naik places Thm 10.20 on p. 122, so Thm 10.13 comes before p. 122. With §10.2 beginning around
  p. 121, Thm 10.13 most likely sits in §10.1, the Mal'cev correspondence for ℚ-powered groups,
  and p. 124 / Example 10.24 transfers it to finite p-groups. This is an inference, not a reading.
  Do not cite "Theorem 10.13" as *the Lazard correspondence* without the book.
- It is not confirmed that Thm 10.13 contains the **subgroup form** (subgroups ↔ Lie subrings)
  that main.tex l.171 cites. Díaz Ramos et al. use only its parts (b), (c), (d). The current
  `\cite[Chapter~10]{Khukhro1998}` is safe. A checkable primary statement of the subgroup form
  in a citable paper is CdGVL §2, p. 434, which lists subgroups ↔ subalgebras and normal
  subgroups ↔ ideals, though without proof.
- **Lemma 9.15: UNCONFIRMED.** One secondary source calls it the explicit BCH formula. Its
  statement was not seen. It concerns the forward formula, not the inverse ones, so it is not
  the right locator for the draft.

**Is "Chapters 9–10" right for (a)?** Yes as a range. If a single pointer is wanted, use
Chapter 10, Lemma 10.7 and §10.2.

### Proposed replacement text
In the proof of Cor. black-box ("Evaluating Φ"), replace
`(the inverse Hausdorff formulas, \cite[Chapters~9--10]{Khukhro1998}; ...`
with one of:
- Safe (needs no book check):
  `(the inverse Baker--Campbell--Hausdorff formulas, \cite[Chapters~9--10]{Khukhro1998} and \cite[\S2]{CicaloDeGraafVaughanLee2012}; ...`
- Precise (one glance at Khukhro pp. 113–124 before submission):
  `(the inverse Baker--Campbell--Hausdorff formulas, \cite[Lemma~10.7 and \S10.2]{Khukhro1998}; see also \cite[\S2]{CicaloDeGraafVaughanLee2012}; ...`

Change the draft's l.24 comment to: "Khukhro locator: inverse formulas = Lemma 10.7 / §10.2
(per CdGVL pp. 433–434 and Naik); book not seen." For main.tex, keep `\cite[Chapter~10]` for the
subgroup form and leave the l.399 marker open until someone checks Thm 10.13 in the book.

## 2. Cicalò, de Graaf, Vaughan-Lee, "An effective version of the Lazard correspondence"

**Bibliographic data: CONFIRMED** from Crossref, zbMATH and the PDF: J. Algebra **352**
(2012), no. 1, 430–450; doi 10.1016/j.jalgebra.2011.11.031; received 6 May 2011, online
22 Dec 2011; communicated by E. O'Brien. The first author's name has a grave accent:
**Cicalò**. No arXiv version exists (arXiv API title search: none). The open copy is the
publisher's PDF in the Trento IRIS repository (handle 11572/90453).

**What it computes (primary, read).**
- §§3–6: algorithms that compute the BCH formula and the two inverse BCH formulas h₁ (Lie sum)
  and h₂ (Lie bracket) up to a fixed weight. The paper says computing the inverse formulas had
  not been considered before.
- §7, p. 442: the input is a p-group G of class below p, **given by a consistent
  power-commutator presentation** on g₁,…,gₙ with relative orders p. The Lie ring is the same set
  G, with g + h = h₁(g,h) and [g,h]_L = h₂(g,h). The algorithm evaluates h₂(g_j,g_i) and
  g_i^p = p·g_i **in G, using the collection algorithm**. It rewrites each result as a sum Σαᵢgᵢ
  through an inductive sum-representation procedure. This yields the Lie ring structure on the
  generators gᵢ (structure constants). The BCH formula then converts between the product and sum
  representations of elements, symbolically if wanted (Hall polynomials, §9.1).
- Abstract: in the converse direction, the BCH formula constructs a p-group from a nilpotent Lie
  ring of order pⁿ and class below p.
- §8: implemented in Magma, with the GAP package LieRing for the Lazard part. The implementation
  handles class ≤ 14, and the authors think class 15–16 at most is feasible. The paper reports
  running times only, with no complexity bound. In LieRing, `PGroupToLieRing` works from a
  `Pcgs`. For exponent p it returns a Lie algebra over GF(p) by structure constants (source:
  `gap/lazard.gi`).

**Draft (A)(c) sentence: CORRECTED (accurate in substance, imprecise in two places).**
- "computes the Lie ring directly from such a presentation": the input is right (a consistent
  power-commutator presentation). "Directly" suggests the method avoids group arithmetic, but it
  multiplies by collection, which is the very cost the draft says it does not analyse.
- The paper does not claim polynomial time. It is a practical method with a fixed class bound
  (≤ 14 in the implementation).
- Attribution point: the draft's "Evaluating Φ" step uses the same mechanism as CdGVL §7, namely
  evaluating truncated inverse BCH words in the group. The paper should credit this rather than
  only say "we do not use it". The draft's additions are the black-box setting, the free-Lie
  pullback, the coherent evaluation and the cost accounting.
- Two more points support the draft's word "fixed". CdGVL p. 434 notes that the inverse formulas
  are not unique: they depend on the ordering chosen for the right-normed commutators. And their
  denominators at weight k involve only primes ≤ k, which gives the draft's r ∈ ℤ[1/c!].

Proposed replacement for the last two sentences of (A)(c):
> We do not analyse the cost of collection. For a $p$-group of class below $p$ given by a
> consistent power-commutator presentation, Cicalò, de Graaf and Vaughan-Lee compute the Lie
> ring structure on the polycyclic generators by evaluating truncated inverse
> Baker--Campbell--Hausdorff formulae in the group with the collection
> algorithm~\cite[\S7]{CicaloDeGraafVaughanLee2012}, and construct the group of a given Lie ring
> by the Baker--Campbell--Hausdorff formula. Their method is practical and is not given a
> complexity bound; the chart acquisition in Corollary~\ref{cor:black-box} evaluates the same
> kind of formulae, but in a black box.

Delete the l.39 marker once the bib entry is added.

Proposed BibTeX entry, in the style of `core/references.bib`:
```bibtex
@article{CicaloDeGraafVaughanLee2012,
  author  = {Cical{\`o}, Serena and de Graaf, Willem A. and Vaughan-Lee, Michael},
  title   = {An Effective Version of the {Lazard} Correspondence},
  journal = {Journal of Algebra},
  volume  = {352},
  number  = {1},
  pages   = {430--450},
  year    = {2012},
  note    = {doi:10.1016/j.jalgebra.2011.11.031}
}
```
(For sentence-case style, use `title = {An effective version of the {L}azard correspondence}`.)

## 3. (A)(a): for n ≤ p the matrix logarithm on UT_n(F_p) is the Lazard logarithm

**Mathematics: CONFIRMED (folklore). Standard textbook citation: UNCONFIRMED; none was found.**
- Grochow–Qiao, arXiv 1907.00309v1, **Proposition 6.5** with a proof sketch: for a p-subgroup
  of GL(d, F_{p^e}), the Lazard Lie ring is realised by the matrix logarithm. Their argument is
  that the first and second inverse BCH formulas hold verbatim with the free nilpotent associative
  algebra replaced by strictly upper-triangular matrices. They point to Khukhro, p. 105
  ("Another remark…"), which falls in Ch. 9. They also state that they could not find a
  convenient reference for the fact. Two caveats:
  1. Their proposition omits the hypothesis d ≤ p (or class below p), which is needed for the
     truncated log to have p-free denominators. The draft's hypothesis n ≤ p is the right one.
  2. The paper was split into SIAM J. Comput. 52(2) (2023) 568–617 and ACM TOCT 16(1) (2024),
     and the proposition's number there was not checked.
- CdGVL §9.2 (p. 448) uses the converse direction: for exponent p and class c < p, the matrix
  exponential of a faithful nilpotent Lie representation with ρ(g)^c = 0 gives a faithful group
  representation, "by the BCH-formula, and the Lazard correspondence".
- The Khukhro p. 105 remark itself was not seen.

Proposed replacement for the sentence in (A)(a):
> The matrix logarithm $\log(I+N) = \sum_{k=1}^{n-1}(-1)^{k+1}N^k/k$ has denominators prime to
> $p$, and $g \mapsto \log g$ is an isomorphism from the Lazard Lie ring of $G$ onto the matrix
> Lie algebra $\log G$: the inverse Baker--Campbell--Hausdorff formulae hold verbatim in the
> algebra of strictly upper-triangular $n\times n$ matrices, since $N^n = 0$ and $n \le p$
> (cf.~\cite[Chapters~9--10]{Khukhro1998} and \cite[Proposition~6.5]{GrochowQiao2019}).

This needs a new bib key: Grochow, Joshua A. and Qiao, Youming, "Isomorphism problems for
tensors, groups, and cubic forms: completeness and reductions", arXiv:1907.00309 (2019). Cite
the arXiv version, whose numbering was checked, or check the SIAM numbering first. The
one-sentence proof in the new text is short enough to stand without a citation if the owner
prefers.

## Summary of verdicts
| Claim | Verdict |
|---|---|
| Khukhro Chs. 9–10 for the inverse Hausdorff formulas | CONFIRMED as a range; the formulas are in Ch. 10 (Lemma 10.7, §10.2; secondary sources: CdGVL, Naik) |
| Khukhro Ch. 10 for the Lazard correspondence | CONFIRMED (Cambridge TOC); §10.2 CONFIRMED by a secondary source (CdGVL) |
| Khukhro Thm 10.13 = Lazard correspondence (subgroup form) | UNCONFIRMED; probably the Mal'cev-section theorem, with Lazard at p. 124 / Ex. 10.24 |
| Khukhro Lemma 9.15 = BCH formula | UNCONFIRMED (one secondary source); forward BCH, so not the draft's locator |
| CdGVL bibliographic data | CONFIRMED; no arXiv version |
| Draft (A)(c) description of CdGVL | CORRECTED (it uses collection, gives no complexity bound, and uses the same inverse-BCH evaluation as the draft) |
| UT_n(F_p), n ≤ p: matrix log = Lazard log | CONFIRMED mathematically; best citation is Grochow–Qiao Prop. 6.5 (arXiv v1), which calls the fact folklore; no textbook theorem found |

Still open for a human with the book: read Khukhro pp. 113–124 to check Lemma 10.7, Thm 10.13
(including whether it has the subgroup form) and §10.2, and p. 105.
