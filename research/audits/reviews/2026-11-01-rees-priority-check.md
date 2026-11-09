# Rees composition: literature-priority check

Date: 2026-11-01. Executed from `research/REES_PRIORITY_BRIEF.md` by a Sonnet 5.5 session at medium effort.
Read-only with respect to the paper, bibliography, notes and registries. This file is the only thing written.
This is a priority check, not a correctness check (see `REES_CORE_PROOF_CHECK_BRIEF.md`).
A missing search hit is not evidence of novelty. Nothing here is a novelty claim.

Downloads: scratchpad `.../scratchpad/pdf/` (PDF via arXiv, text via `pdftotext -layout`).
"Read" means the abstract, introduction, the statements and proofs of the theorems named, and the concluding
section where one exists. No paper was read end to end.

## 0. Bottom line

- Conjunction (A1+A2+A3+A4+A5): **Possibly new in the stated regime.** No covering theorem was found.
  The regime is: finite p-group G of fixed class c < p given by an explicit Lazard Lie algebra over F_p,
  arbitrary hidden subgroup H, bounded-error algorithm, p unbounded (polynomial in log p), no bound on exponent
  or derived length. The search was thin (see section 4 and 7).
- Closest prior results, none covering the regime:
  1. Imran–Ivanyos (arXiv:2304.08376, Thm 1): arbitrary H, any fixed class, **primes of |G| bounded by a constant**,
     black-box unique encoding, exact. Their authors write that, for class above two, the needed automorphisms
     "do not exist in general".
  2. Ivanyos–Santha (arXiv:1503.09016, Cor 8): p unbounded, fixed class, but only the groups F_p ⋉ F_p^m and
     only hidden subgroups of order p outside F_p^m.
  3. Ivanyos–Sanselme–Santha (arXiv:0707.1260): scalar-weight twisting with a quadratic-plus-linear equation
     system, class two only.
- Two items need Opus review (section 5): (a) whether IS Cor 8 covers A2 or A4, (b) the status of the
  Imran–Ivanyos result for smooth order. My provisional reading: (a) no; (b) conditional for non-constant primes,
  smooth order is posed as an open problem.
- Both 2026 arXiv IDs resolve. Titles and authors match the repo bibliography. Neither bears on A1–A5 as a
  covering result.

## 1. Sources table

| Key | Fetched as | Label | Theorem/section numbers used |
|---|---|---|---|
| ISS2012 | arXiv:0707.1260v1, 12 pp | FULL TEXT | Thm 1 (nil-2 HSP); Prop 1 (maps φ_j); Thm 2 and Cor 1 (classical reduction); Lemmas 5–6; Thm 5 (quadratic-plus-linear system) |
| IS2015/2017 | arXiv:1503.09016v2 (8 Jun 2016, TCS accepted version), 16 pp | FULL TEXT | Def 4; Thms 3 and 5; Cor 6; Prop 7; **Cor 8**; Sections 3.1–3.3, 4.1; Thm 11 |
| ImranIvanyos | arXiv:2304.08376v1 (only arXiv version) and the QIP 23:14 author manuscript (eprints.sztaki.hu/10704) | FULL TEXT, both | **Thm 1**; Lemma 2; Props 1–3; Thm 2; Sec 5 closing remark; **Sec 6** |
| DHIS14 | arXiv:1305.1543v2 | FULL TEXT (Intro, Thms 1–3, Cor 4) | Thm 3 and Cor 4 need m, r, D constant |
| FIMSS14 | arXiv:quant-ph/0211091v4 | FULL TEXT (abstract, intro, Thm 4.16 statement) | Thm 4.16 ("smoothly solvable") |
| IMS2001 | arXiv:quant-ph/0102014v1 | FULL TEXT (abstract, **Thm 11** statement and proof opening) | Thm 11 |
| HRT2003 | not fetched | NOT FETCHED | SICOMP, paywalled. Used only as background, so no verdict depends on it. |
| Morales2026 | arXiv:2608.05321 (abs page and PDF fetched) | FULL TEXT (abstract, intro, App. A.3) | abstract; A.3 comparison with bounded class |
| HoltSubramanian2026 | arXiv:2609.38085 (abs page and PDF fetched) | FULL TEXT (abstract, intro, headings) | abstract: normal H only |
| ePrint 2026/2678 (HSP survey, Di Concilio et al.) | 403 on fetch | SNIPPET only | not usable as evidence |
| AIMS Math 2026, 11(4):9380 (Dong–Fan–Zhong–Qiu) | WebFetch of publisher page | ABSTRACT | generating-set bounds for nilpotent groups. Only abelian-HSP application. Not relevant. |

arXiv confirmation of the 2026 IDs (abs pages, fetched 2026-11-01):
- 2608.05321: "The Hidden Subgroup Problem in Semidirect Products and Quasi-Hamiltonian Groups", Morales, Mauro E. S.;
  dated 2026/08/05, online 2026/09/28. Matches the bib.
- 2609.38085: "Learning quantum symmetries", Holt, Isaac; Subramanian, Sathyawageeswar; dated 2026/09/29.
  Matches the bib.

## 2. Verdicts

Overlap marks follow brief P3. "Hyp" means hypotheses.

**A1 (Rees homogenization): Possibly new in the stated regime.**
No source found that makes an arbitrary H invariant under graded dilations of a nilpotent group by a Rees tuple
cover with c evaluations per source.
- ISS Prop 1 and Lemma 5(2) use the automorphisms φ_j, whose action on a hidden element h contributes the term
  `ω^{<u,z_h>(j−j²)}`. The "correction for hidden elements" appears there as a linear term. Overlap in technique,
  c = 2 only.
- Imran–Ivanyos Lemma 2 converts central sources for arbitrary H by zero-sum subsequences (binary weights).
  Overlap in goal (arbitrary H, central cancellation), different mechanism.
- The Rees construction and the Lazard correspondence were treated as standard in the brief and not searched.
- No hit for Rees, graded dilation or Lazard in the HSP literature (queries Q1, Q3, Q9).

**A2 (central descent by scalar weights): Partly known.** Needs Opus review (a).
- Known: cancelling central characters with scalar-weighted twists and solving a diagonal system. ISS Lemma 5 and
  Thm 5 do this for c = 2, with weights j, j² and a quadratic-plus-linear system.
  IS Thm 3 is the fixed-degree diagonal-equation solver (n > d^{d log d}(m+1)^{d log d}).
- Not found: iteration through grades c, …, 2 with scalar weights s^d for arbitrary H at class above two.
  Imran–Ivanyos (Sec 1, Related results) say that automorphisms that "do not change the hidden subgroup too much"
  "do not exist in general nilpotent groups of class greater than two".
- Imran–Ivanyos Sec 5 closing remark: the IS algorithm for "dth power coefficients" contains zero-sum as the case
  d = p−1, giving S(p,n) = p^{O(p log² p)} n^{O(p log² p)}, polynomial in n only for p = O(1).
  This is the closest published statement about weights of degree d in the HSP context.

**A3 (readout): Partly known.**
The abelian step is standard. ISS (recovering HG′) and Imran–Ivanyos (Prop 2, exact abelian HSP on G/G′) both
finish with an abelian HSP. That the grade-one state hides log H exactly for arbitrary H depends on A1+A2 and is
therefore as new as they are.

**A4 (growing prime): Partly known.** Needs Opus review (a).
- Known: p unbounded at fixed class, but only for F_p ⋉ F_p^m with H of order p not contained in F_p^m
  (IS Cor 8, via Prop 7 and Cor 6). DHIS14 had this for m constant (Thm 3, Cor 4).
- Known: arbitrary H at fixed class when primes are bounded by a constant (Imran–Ivanyos Thm 1).
- Not found: arbitrary H at fixed class with p growing for any group beyond those two.
- First theorem that would make A4 non-novel if its hypotheses were relaxed: IS Cor 8, if one reads the
  restriction on H as removable. That is not in the text (see 5a).

**A5 (complexity, no bound on primes, exponent or derived length): Possibly new in the stated regime.**
- FIMSS Thm 4.16 needs bounded exponent and bounded derived length ("smoothly solvable").
  A Lazard group of exponent p, with p growing, is outside it.
- IMS Thm 11 is poly(input size + |G′|). |G′| is large for class three or more, so it does not apply.
- Imran–Ivanyos Thm 1 needs bounded primes.
- IS Cor 8 is restricted to one group family and one hidden-subgroup family.
- Morales covers scalar-action semidirect products and quasi-Hamiltonian groups, not Lazard groups of general class.
- Input-model difference: A5 assumes an explicit Lazard Lie algebra with bounded error. Imran–Ivanyos assume a
  black-box group with unique encoding and give an exact algorithm. This is a difference in regime, not a gap in
  the prior work. Any comparison must say so.

**Conjunction: Possibly new in the stated regime.** Conditions: fixed class c < p, explicit Lazard Lie algebra
input, arbitrary H, bounded error, p unbounded. This is not a "Known" or "Partly known" for the whole composition
because no source covers A1 or A5. It is "Partly known" at the level of ingredients (A2 at c = 2, A3, the SDE solver).

Open-problem link: Imran–Ivanyos Sec 6 poses "a poly(np)-time algorithm for finding zero sum subsequences from
sequences of length (np)^d" as a problem for further research. If the Rees composition is correct, it answers the
HSP consequence of that question in a different input model, not the zero-sum question itself.

## 3. Test of the paper's characterizations (P4)

Each sentence in `main.tex` lines 110–113 and 116 and `REES_HSP_REDUCTION.md` Section 7 was compared with the text.

| Paper statement | Verdict | Correct statement or note |
|---|---|---|
| ISS: nil-2 polynomial time; twisted right actions correct for hidden elements (Prop 1, Lemmas 5–6) | Accurate | Prop 1 gives φ_j(z) = z^{j²} on G′ and φ_j(g) = g^j z_g^{j−j²}. Lemma 5(2) gives the eigenvalue ω^{<u,z_h>(j−j²)}. Lemma 6 gives a hiding set for HG′. |
| ISS also has a classical reduction | **Omitted** | Thm 2: for a class of groups of constant class closed under subgroups and quotients, the HSP reduces to p-groups of exponent p with H trivial or of order p. Lazard groups over F_p have exponent p, so this theorem bears on the setting. Consider citing it. |
| DHIS14: F_p ⋉ F_p^m of constant class with p growing, hidden subgroups of order p not contained in F_p^m | **Inaccurate** | DHIS14 Thm 3 and Cor 4 require m, r, D constant, and the HSP link is only for Z_p^m ⋊ Z_p via an earlier paper. IS17 says: "In [9] ... HPGP′ (F_q,1,m,d) is solvable ... when d and m are both constant" and that Thm 3 lets one "dispense ... with the assumption that m is constant". The arbitrary-m statement is IS17 Cor 8. |
| IS17 Cor 8: F_p ⋉ F_p^m of constant class, hidden subgroups of order p not in F_p^m | Accurate, but see below | The restriction on H is in Def 4 and the surrounding text (family of subgroups of order p not in 0 × F_p^m), not repeated in the printed Cor 8. |
| IS17 gives a fixed-degree SDE algorithm (Section 3) | Accurate | Thm 3, Sections 3.1–3.3. The abstract and intro also state a deterministic algorithm; only the warm-up Props 9–10 are randomized (intro text). The exact arity constants in `main.tex` eq. `is-arity` were not checked against Thm 11. |
| Imran–Ivanyos Thm 1: exact HSP, nilpotent, bounded class, bounded prime factors | Accurate | Black-box group with unique encoding; poly(ℓ) operations, poly(log|G|) oracle calls. |
| Imran–Ivanyos convert central sources for arbitrary H by zero-sum subsequences (Lemma 2) | Accurate | Lemma 2 needs an exact zero-sum method for S(p,n) vectors. |
| Imran–Ivanyos concluding section "asks for an efficient, possibly non-exact, algorithm for bounded class and smooth order" | **Slightly compressed** | Sec 6 asks for a poly(np)-time zero-sum algorithm on sequences of length (np)^d. A positive answer gives an exact algorithm for smooth |G|. A randomized version would give a non-exact one (via Prop 3). The paper's sentence mixes the two. |
| FIMSS: solvable, bounded derived length, bounded exponent | Accurate | Thm 4.16, "smoothly solvable". Also gives subexponential time for every solvable group. |
| IMS Thm 11: poly(input + |G′|) | Accurate | The theorem needs |G′| small to be efficient. |
| Morales: A ⋊ Z_{p^k} with scalar action and quasi-Hamiltonian groups | Accurate but incomplete | The abstract adds: bounded generator rank and Exp(A)/p = polylog(|G|) for the first family; the second is "under a mild assumption on the input structure". |
| Holt–Subramanian: state HSP for normal hidden subgroups | Accurate | Abstract: non-abelian StateHSP "when the hidden subgroup is normal". |
| The free class-three example lies in neither Morales family | Not tested | A mathematical claim outside this brief. Mark for the proof check. |

Morales independently describes the Imran–Ivanyos result as "efficient if the prime factors of the order are bounded
by a constant" (Morales Sec 1 and App. A.3). This is secondary evidence for 5b.

## 4. Search log

All dates 2026-11-01. Mode `standard` unless stated. "Rel." counts results of about 10 that were relevant
to HSP in nilpotent groups. The tool returns about 10 links per query, and they overlap heavily.

| # | Query | Rel. | Notes |
|---|---|---|---|
| Q1 | hidden subgroup problem p-group "class less than p" quantum polynomial time Lazard | 4 | IMS01, ISS, EHK, nothing on Lazard |
| Q2 | hidden subgroup nilpotent bounded class large prime quantum algorithm zero sum subsequences follow-up | 3 | only Imran–Ivanyos and mirrors; no follow-up |
| Q3 | non-abelian hidden subgroup Rees construction graded dilation central character Fourier nilpotent class three | 2 | only ISS; no Rees hit |
| Q4 | diagonal polynomial equations hidden subgroup nilpotent quantum 2024 2025 2026 | 2 | only IS17 and mirrors; no 2024–2026 hit |
| Q5 | arXiv 2304.08376 "Zero sum subsequences and hidden subgroups" cited hidden subgroup nilpotent groups | 1 | "no citations found" by a mirror site. Weak evidence. |
| Q6 | Ivanyos Santha "Solving systems of diagonal polynomial equations over finite fields" hidden subgroup semidirect nilpotency class citations | 1 | publication data only |
| Q7 | Imran Ivanyos "Zero sum subsequences and hidden subgroups" Quantum Information Processing 2024 volume 23 article 14 | 1 | confirmed QIP 23:14, DOI 10.1007/s11128-023-04228-2 |
| Q8 | quantum algorithm hidden subgroup nilpotent groups Lie algebra Lazard correspondence grading automorphisms | 2 | no Lazard or grading hit |
| Q9 | "hidden subgroup problem" nilpotent groups smooth order constant class randomized zero-sum algorithm Davenport constant | 1 | only Imran–Ivanyos |
| Q10 (extended) | quantum algorithm hidden subgroup problem nilpotent group class three growing prime exponent p arbitrary hidden subgroup new result 2025 2026 | 3 | Morales, 2026 survey (ePrint 2026/2678, 403), AIMS Math paper (irrelevant). No class-3 growing-p result. |

Not run: the brief's queries "hidden subgroup" "Lazard correspondence" (covered by Q1, Q8), the Morales-specific
query (the arXiv abs page was fetched directly instead). No Google Scholar, Semantic Scholar or arXiv "cited by"
listing was reachable, so citing-paper coverage for 2304.08376 and 1503.09016 is **not** established.
The one mirror that reports "no citations" is weak evidence.

Side hits not read, listed for completeness: arXiv:quant-ph/0412033 (HSP over a class of semidirect products),
arXiv:quant-ph/0211124, arXiv:1509.05806 (hypergroups and nilpotent hidden normal subgroups), arXiv:quant-ph/0503095.
None looked like a bounded-class, arbitrary-H result from the snippets. Snippets are not evidence.

## 5. Judgement calls: needs Opus review

### 5a. Does Ivanyos–Santha Cor 8 cover A2 or A4?

Primary text (arXiv:1503.09016v2), exact quotations.

Def 4 (p. 4): "The hidden subgroup problem HSP is parametrized by a finite group G and a family H of subgroups of G.
HSP(G, H) — Oracle input: A function f from G to some finite set S. Promise: For some subgroup H ∈ H, we have
f(x) = f(y) ⟺ Hx = Hy. Output: H."

Intro (p. 4): "Bacon, Childs and van Dam in [5] have considered the HSP in p-groups of the form G = F_p ⋉ F_p^m when the
hidden subgroup belongs to the family H of subgroups of order p which are not subgroups of the normal subgroup
0 × F_p^m. They have found an efficient quantum algorithm for such groups as long as m is constant."

"Proposition 7. Let d be the nilpotency class of a group G of the form F_p ⋉ F_p^m. There is a polynomial time quantum
algorithm which reduces HSP(G, H) to HPGP′(F_p, 1, m, d)."

"Corollary 6. If d is constant then HPGP′(F_p, 1, m, d) is solvable in quantum polynomial time."

"Corollary 8. If the nilpotency class of the group G of the form F_p ⋉ F_p^m is constant then HSP(G, H) can be solved
in quantum polynomial time."

Section 4.1: "Then H, the family of subgroups of G_B of order p which are not subgroups of N is exactly
{H_v : v ∈ F_p^m}."

My reading:
- Cor 8 has p unbounded and the class constant, so it overlaps A4's growth of p, but only for the group family
  F_p ⋉ F_p^m (an abelian normal subgroup of index p) and the family of H of order p not in F_p^m.
  It does not address arbitrary H. A2 (grade-by-grade cancellation with scalar weights) is not in its proof;
  the proof is a reduction to a hidden polynomial graph problem solved with the SDE solver.
- Possible reading against this: a Lazard group with c < p contains such F_p ⋉ F_p^m groups as special cases, so A4 is
  "partly known" for that sub-family. I treated it so. Whether the paper should say "special case of the regime"
  is a mathematical judgement for Opus. I did not check whether every such G is a Lazard group of class < p
  (B^p = I gives class at most p, possibly equal to p).

Provisional ruling: A2 not covered; A4 partly covered (special groups, restricted H). **Needs Opus review.**

### 5b. Imran–Ivanyos: unconditional for smooth order, or conditional on a zero-sum method?

Primary text (arXiv:2304.08376v1; the QIP 23:14 author manuscript has the same wording in Sec 6 and Thm 1):

Abstract: "We present a new deterministic polynomial time algorithm for the latter problem in the case when the size
of the field is constant. The consequence is a polynomial time exact quantum algorithm for the hidden subgroup
problem in nilpotent groups having constant nilpotency class and whose order only have prime factors also bounded by
a constant."

Thm 1: "Suppose that G is a nilpotent group of class bounded by a constant and that the prime factors of |G| are also
bounded by a constant. We assume that G is a black-box group with unique encoding of elements by ℓ-bit strings. Then
there is an exact quantum algorithm that solves the hidden subgroup problem in G using poly(ℓ) operations and
poly(log|G|) calls to the subgroup state creating oracle and its inverse."

Prop 2 (HSMC): "Assume that ... we have an exact method to find zero sum subsequences of sequences of S(p,n) elements
of Z_p^n in time T(p,n) ≥ S(p,n). Then the problem HSMC can be solved by an exact quantum algorithm that uses
poly(T(p,n)^{O(c)} ℓ) elementary operations ..."

Thm 2 (Sec 5): "There is a deterministic algorithm that, given a sequence of S(p,n) = p^{O(p log² p)} n^{O(p log² p)}
vectors from Z_p^n, finds a non-trivial zero sum subsequence in time poly(S(p,n))."

Sec 6: "We have shown that the hidden subgroup problem in a nilpotent group G of class bounded by a constant can be solved
in polynomial time by an exact quantum algorithm provided that there is a polynomial time (that is, time poly(n log p))
exact method that finds zero sum subsequences in sequences consisting of polynomially many elements of Z_p^n for prime
divisors p of |G|. We have such a method for p = O(1)."

"We propose the question of existence of a poly(np)-time algorithm for finding zero sum subsequences from sequences of
length (np)^d for a sufficiently large constant d as a problem for further research. A positive answer would imply
existence of an exact polynomial time quantum algorithm for the case when |G| is smooth, that is, the prime factors of
|G| are of size bounded by a polynomial in log|G|."

Reading: the third-party summaries are each half right. Thm 1 is unconditional **for constant primes**, because Thm 2
supplies the zero-sum method there. For larger primes the result is conditional on a zero-sum method (Sec 6 first
sentence). For smooth order it is not claimed at all; it is posed as an open problem that a positive answer would
settle. The paper (main.tex) cites Thm 1 as unconditional "whose prime factors are bounded": that is accurate.
Its sentence about the concluding section is a compression (see section 3).

Provisional ruling: not unconditional for smooth order. **Needs Opus review.**

## 6. Growing-prime regime and barriers (P6, P7)

P6. The strongest bound on primes for arbitrary H at fixed class that I found is a **constant** (Imran–Ivanyos
Thm 1). The only growing-p results found are IS Cor 8 and DHIS14 (restricted groups and restricted H). The first
theorem that would make A4/A5 non-novel would be a bounded-class, unbounded-prime, arbitrary-H result. None found.
Imran–Ivanyos Sec 5 remark gives the reason their route is stuck: zero-sum by an SDE needs d = p−1.

P7. I read only the status headers and the opening of each barrier note, not the notes in full:
- `BOUNDED_CLASS_METABELIAN_HSP.md`: "Local proposed composition, not an independently reviewed theorem".
- `CLASS_FOUR_HSP_THEOREM_DRAFT.md`: "PROPOSED THEOREM AND PROOF DRAFT, not an admitted result".
- `BOUNDED_CODIMENSION_HSP_REDUCTION.md`: "LOCAL PROOF; independent review pending"; relies on the Rees route.
- `AMBIENT_SECTION_POTENTIAL.md`: "Not a complete HSP algorithm".
All four are internal, unreviewed proposals. None cites a published barrier result in the parts I read.
The only published algorithm they lean on is the nil-2 result (ISS) for k ≤ 2.
I did not find a "growing-class barrier" stated as a published theorem. Whether any internal note states a barrier
that the Rees route must respect was not established by this pass.

## 7. Bibliography mismatches (P8, not fixed)

Ivanyos–Santha, key `IvanyosSantha2015`:
- Key and `main.tex` use "2015" (`\cite{IvanyosSantha2015}`); the entry has `year = {2017}`; the note names the FAW 2015
  extended abstract. The rendered year will follow the entry, so the text cites 2017 while the key says 2015.
- Entry title is the TCS title "Solving Systems of Diagonal Polynomial Equations over Finite Fields". The FAW abstract is
  titled "On solving systems of diagonal polynomial equations over finite fields". arXiv v1 (31 Mar 2015) carries the FAW
  title; v2 (8 Jun 2016) is the TCS accepted version.
- Venue facts confirmed from the paper itself: TCS 657 (2017), pp. 73–85 (per Imran–Ivanyos ref [IS17] and a publisher
  index). DOI 10.1016/j.tcs.2016.04.045 (on the arXiv v2 title page, "© 2016"). FAW 2015, LNCS 9130, pp. 125–137.
  The DOI year (2016 online) and volume year (2017) differ. Not fixed.
- `main.tex` cites "[Corollary 8]" and "[Sections 3.1–3.3]" for the TCS numbering. These match arXiv v2. The FAW extended
  abstract was not seen, so numbering there is unchecked.

Other entries:
- `ImranIvanyos2023`: key year 2023 (arXiv), entry year 2024 (QIP 23:14, published online 5 Jan 2024). Consistent
  apart from the key. Only an arXiv v1 exists as of today.
- `DeckerHoyerIvanyosSantha2014`: QIC 14(9–10) 790–806 matches the Imran–Ivanyos reference list.
- `FIMSS2014`: SICOMP 43(1):1–24 matches the Imran–Ivanyos reference list. The arXiv version is quant-ph/0211091, not
  listed in the entry. Imran–Ivanyos add "Preliminary version in STOC 2003".
- `IvanyosSanselmeSantha2012`: Algorithmica 62(1–2):480–498 matches.
- `IvanyosMagniezSantha2001`: entry is `@misc` with arXiv only; the work also appeared at SPAA 2001. Not verified.
- `HallgrenRussellTaShma2003`: not fetched; only confirmed through citations in Morales and Imran–Ivanyos.

## 8. Proposed wording for the related-work paragraph (main.tex line 116)

A proposal only. The paper is not edited.

> We compare with nearby results by scope only. Ivanyos, Sanselme and Santha solve the HSP in nilpotent groups of
> class two by twisting right actions by automorphisms, and give a classical reduction for constant class to
> exponent-p groups with hidden subgroup of order at most p [ISS12, Thm 2]. Friedl, Ivanyos, Magniez, Santha and
> Sen solve it for solvable groups of bounded exponent and bounded derived length [FIMSS14]; here the exponent p grows.
> Ivanyos and Santha [IS17, Cor 8] treat F_p ⋉ F_p^m of constant class, with p growing, for hidden subgroups of order p
> not contained in F_p^m; Decker, Høyer, Ivanyos and Santha [DHIS14] treat this with the dimension m constant.
> Imran and Ivanyos [II24, Thm 1] solve the HSP exactly, for arbitrary hidden subgroups, in black-box nilpotent groups
> of bounded class whose prime factors are bounded by a constant; their method is conditional on a zero-sum
> subsequence algorithm for larger primes, and they pose the smooth-order case as an open problem [II24, Sec 6].
> They also note that automorphisms that nearly preserve the hidden subgroup do not exist in general beyond class
> two [II24, Sec 1]. Morales treats scalar-action semidirect products A ⋊ Z_{p^k} with bounded generator rank and
> quasi-Hamiltonian groups under an input assumption [Mor26]. Holt and Subramanian treat the state HSP for normal
> hidden subgroups [HS26]. We found no result covering fixed-class Lazard p-groups with p growing and an arbitrary
> hidden subgroup, but our search was limited and this is not an exhaustive literature review.

## 9. What an expert must still check

1. Rulings 5a and 5b (Opus).
2. Citation tracking: forward citations of arXiv:2304.08376 and arXiv:1503.09016 on Google Scholar or Semantic Scholar
   (not reachable here); the QIC/FAW versions of IS17; the SPAA 2001 version of IMS.
3. The published QIP version's Section 6 against the arXiv v1 (checked: same wording in the author manuscript, which is
   not the typeset version).
4. Whether the F_p ⋉ F_p^m groups of Cor 8 are Lazard groups of class < p, and whether A4 should be called a
   strict generalization of Cor 8 on that family.
5. The arity constants of `main.tex` eq. `is-arity` against IS17 Thm 3 and Thm 11. Thm 3's stated bound is
   n > d^{d log d}(m+1)^{d log d}; the paper uses [d^{d(d−1)/2}(a+1)^d]^{⌈log₂(d+1)⌉}. Not compared (proof-check scope).
6. The claim that the free two-generator class-three Lazard group is in neither Morales family (not tested here).
7. A search of group-theory and Lie-algebra literature for a Rees or graded-cover method used with oracles.
   This pass searched only HSP and quantum-algorithm literature.
8. A second look at ISS Thm 2 (classical reduction to exponent p, H trivial or of order p) as possibly simplifying or
   preempting part of A1.
9. P7: read the four internal barrier notes beyond their headers if the question of which barriers are published
   matters for the claim gates.
