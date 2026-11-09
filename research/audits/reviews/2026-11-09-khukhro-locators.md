# 2026-11-09 Khukhro (1998) locators: checked against the book's own pages

Scope: exact theorem and page locators in E. I. Khukhro, *p-Automorphisms of Finite
p-Groups*, LMS LNS 246, CUP 1998 (bib key `Khukhro1998`), for (a) the inverse BCH formulas,
(b) the forward BCH formula, (c) the Lazard correspondence and its subgroup form, and (d) their
pages. This follows up `2026-11-09-rees-blackbox-citation-check.md`, which had to rely on
secondary sources. No file other than this report was edited, and no git actions were taken.

## Access used (legitimate, publisher-authorised preview only)

- **Google Books partial preview**, volume `wFhQ6uIOU_UC`, with pages "displayed by permission
  of Cambridge University Press". The 26-page preview contains these pages of Chs. 9–10:
  pp. 102–106, 109, 111, 113–115, 117, 119–121 and 124–128. I read them as page images in the
  Claude browser pane. They were not saved or downloaded.
  - Page view: https://books.google.com/books?id=wFhQ6uIOU_UC&pg=PA115
  - Search inside: https://books.google.com/books?id=wFhQ6uIOU_UC&q=Lazard
- **Google Books search-inside snippets** reach pages outside the preview (p. 107, p. 118).
  pp. 108, 110, 112, 116 and 122–123 are neither in the preview nor in the snippet index.
- The printed page numbers in the preview images match Google's `PA` numbers. For example,
  image PA121 carries running head "10.2. The Lazard Correspondence 121". They also match the
  Cambridge Core chapter ranges (Ch. 9 pp. 101–112, Ch. 10 pp. 113–129).

## Results

### (a) Inverse Baker–Hausdorff formulas: **Lemma 10.7, p. 115 (§10.1)**. CONFIRMED from the book's text.
- p. 114 (§10.1). The book derives the inversions of the Baker–Hausdorff formula from
  Theorem 10.4 (√F = e^{ℚL}, also on p. 114). These are displays (10.5)–(10.6). They give
  e^{x+y} = h₁(e^x, e^y) and e^{[x,y]} = h₂(e^x, e^y), where h₁, h₂ are ℚ-powered group words.
- p. 115. The book names (10.6) the *Inverse Baker–Hausdorff Formulae*. **Lemma 10.7** gives
  their form:
  - (a) h₁ = e^{x₁}e^{x₂}∏κ_j^{r_j}, with r_j ∈ ℚ and κ_j group commutators of weight ≥ 2
    taken in order of increasing weight;
  - (b) h₂ = [e^{x₁}, e^{x₂}]∏κ_j^{s_j}, with s_j ∈ ℚ and weight ≥ 3.
- p. 117 (§10.1). The Lie ℚ-algebra L_G is defined on the set of a nilpotent ℚ-powered group
  G by g₁+g₂ = h₁(g₁,g₂) and [g₁,g₂] = h₂(g₁,g₂).
- p. 118 (snippet). The text says that Lemmas 9.15 and 10.7 are restated next, as **Lemma 10.12**.
  Its part (a) reads a+b = h₁(a,b) = ab∏κ_j^{r_j} inside a correspondence pair G = M.
- p. 121, **Remark 10.15**. The inverse formulas are unique for a fixed ordered sequence of
  basic commutators. This bears on the draft's word "fixed", and it matches CdGVL p. 434.
- p. 124 (§10.2). In the Lazard setting the same h₁, h₂ define the Lie operations, with all
  coefficients and exponents in ℚ_π, where π is the set of primes ≤ c (the book writes π(c!)).
- Cross-check: CdGVL (J. Algebra 352, 2012) cites Lemma 10.7 on p. 433, and Naik's thesis also
  cites it. Both agree with the book.

### (b) Forward BCH (Baker–Hausdorff) formula: **§9.2, pp. 104–109**. CONFIRMED from the book's text. The Lemma 9.15 page is UNCONFIRMED.
- §9.2 "The Baker–Hausdorff Formula" begins on **p. 104**, and §9.3 begins on **p. 109**
  (both seen).
- **Definition 9.6, p. 105**: H(x₁,x₂) = log(e^{x₁}e^{x₂}). The book notes that the theorem
  "H ∈ ℚL" is what is usually called the Baker–Hausdorff Formula.
- **Theorem 9.11, p. 107** (snippet): H(x,y) ∈ ℚL.
- **(9.16), p. 109**: the explicit Dynkin-type expansion of H(x,y) as a combination of
  commutators.
- **Remark 9.17, p. 109**: no prime divisor of a denominator exceeds c. This is the
  book-level source for the ℤ[1/c!] claim at main.tex l.398.
- **Lemma 9.15**: it exists in §9.2. The p. 118 snippet, which restates Lemmas 9.15 and 10.7 together as Lemma 10.12, shows that
  it is the forward-direction companion of Lemma 10.7, and Lemma 10.12 restates both. Its
  statement and page were **not seen**. It lies between Corollary 9.14 and (9.16), so it is on
  p. 108 or at the top of p. 109. p. 108 is outside both the preview and the snippet index.
  Verdict: the number is CONFIRMED to exist, the page and content are UNCONFIRMED. Díaz Ramos
  et al. (arXiv 1612.06584) call it the explicit BCH formula. Do not cite Lemma 9.15 for a
  specific statement. Cite §9.2, Theorem 9.11 or (9.16) and Remark 9.17 instead.

### (c) Lazard correspondence and its subgroup form: **§10.2, p. 124 (general construction and Example 10.24), with Theorem 10.13 (p. 119) transferred by the p. 124 remark**. CONFIRMED from the book's text.
- **Theorem 10.13, p. 119** (proof ends on p. 120) is the **Mal'cev** correspondence in §10.1.
  It is stated for nilpotent ℚ-powered groups and nilpotent Lie ℚ-algebras, not for finite
  p-groups. Its parts are:
  - (a) ℚ-powered subgroups ↔ Lie ℚ-subalgebras;
  - (b) normal ↔ ideals;
  - (c) abelian and central sections;
  - (d) equal nilpotency class;
  - (e) equal derived length;
  - (f) Aut G = Aut M as permutation groups;
  - (g) freeness.
- **§10.2 "The Lazard Correspondence" begins on p. 121** (heading seen mid-page). It contains
  σ-divisibility, Example 10.17 (a p-group is p′-divisible and p′-torsion-free) and
  Lemma 10.18 on p. 121.
- **p. 124**. Here the book states the Lazard correspondence: nilpotent Lie ℚ_π-algebras of
  class ≤ c correspond to nilpotent ℚ_π-powered groups of class ≤ c, through h₁, h₂ and H on the
  same underlying set. Lemma 10.12 continues to hold, and the book adds "An analogue of Theorem
  10.13 can be proved in exactly the same way."
- **Example 10.24, p. 124**. A finite p-group of class ≤ p−1 corresponds to a nilpotent Lie ring
  of class ≤ p−1 whose additive group is a p-group. It also gives the **subgroup form** for finite
  p-groups: every abstract (normal) subgroup of P is automatically π-divisible, hence a Lie
  ℚ_π-subalgebra (ideal) of M = L_P. It also gives [M,M] = [P,P].
- So the citation "Theorem 10.13 and page 124" (Díaz Ramos et al.) is **accurate**: Theorem 10.13
  is the template, and p. 124 transfers it to the Lazard / finite-p setting. The other source's
  "Theorem 10.20 on p. 122" (Naik) could not be checked. pp. 122–123 are not in the preview or
  the snippet index, and "Theorem 10.20" returns no snippet. Lemma 10.18 is at the foot of
  p. 121 and Example 10.24 is on p. 124, so Theorems 10.19–10.23 fall on pp. 122–123. Naik's
  page is consistent with that but UNCONFIRMED. Naik's Theorem 10.20 concerns π-powered hulls,
  which is not the subgroup form, so it is not needed for the paper's claims.
- Not found explicitly: the claim γ_k(G) = γ_k(L) for all k (main.tex l.398). The book gives
  equal class (Thm 10.13(d) analogue) and [P,P] = [M,M] (Ex. 10.24). The full equality was not
  seen stated in the pages read. Keep that claim attributed to Lazard1954, or prove it from
  10.13(c) applied inductively.

### (d) Page summary

| Item | Locator | Page | Verdict |
|---|---|---|---|
| Ch. 9 / Ch. 10 | chapters | 101–112 / 113–129 | CONFIRMED (Cambridge Core TOC; book pages) |
| Forward BCH defined | §9.2, Def. 9.6 | 104 (§ start), 105 | CONFIRMED (book text) |
| BCH is a Lie element | Thm 9.11 | 107 | CONFIRMED (book snippet) |
| Explicit BCH; denominators ≤ c | (9.16), Remark 9.17 | 109 | CONFIRMED (book text) |
| Lemma 9.15 | §9.2 | prob. 108 | number CONFIRMED (p. 118 snippet); content and page UNCONFIRMED |
| Inverse BCH formulas | (10.5)–(10.6), Lemma 10.7 | 114–115 | CONFIRMED (book text) |
| Restatement in a correspondence pair | Lemma 10.12 | 118 | CONFIRMED (book snippet) |
| Mal'cev correspondence properties, incl. subgroups ↔ subalgebras | Thm 10.13 | 119–120 | CONFIRMED (book text) |
| Uniqueness of h₁, h₂ | Remark 10.15 | 121 | CONFIRMED (book text) |
| §10.2 Lazard correspondence begins | §10.2 | 121 | CONFIRMED (book text) |
| Thm 10.20 | §10.2 | 122 (Naik) | UNCONFIRMED (page not accessible) |
| Lazard correspondence over ℚ_π; analogue of 10.13 | §10.2 | 124 | CONFIRMED (book text) |
| Finite p-groups, class ≤ p−1; subgroups ↔ subalgebras, normal ↔ ideals | Example 10.24 | 124 | CONFIRMED (book text) |

## Recommended citation text

(a) Inverse formulas (appendix-torsion-blackbox.tex l.94 and the draft corollary's "Evaluating Φ"):
`\cite[Lemma~10.7, p.~115]{Khukhro1998}`. For the class-below-p version use
`\cite[Lemma~10.7 and \S10.2, pp.~115 and~124]{Khukhro1998}`. Uniqueness for a fixed ordering
of basic commutators is `\cite[Remark~10.15]{Khukhro1998}`.

(c) Lazard correspondence and its subgroup form (main.tex l.171; main-core.tex l.135, l.215):
`\cite[Theorem~10.13 and Example~10.24, pp.~119 and~124]{Khukhro1998}`. Where only the
correspondence itself is meant, `\cite[\S10.2, Example~10.24]{Khukhro1998}`.
Wording note: Theorem 10.13 is stated for the Mal'cev (ℚ-powered) case. Write "see the analogue
of Theorem 10.13 in §10.2 and Example 10.24", not "Theorem 10.13 (Lazard correspondence)".

Forward BCH and denominators (main.tex l.398): `\cite[\S9.2, Theorem~9.11 and Remark~9.17]{Khukhro1998}`.

The `NEEDS HUMAN VERIFICATION` marker at main.tex l.399 can be narrowed. The Chapter 9–10
locators are now checked against the publisher-authorised preview. What remains open is (i) the
statement and page of Lemma 9.15 (not used) and (ii) a book locator for γ_k(G) = γ_k(L), which
was not found.
