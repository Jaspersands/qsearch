# Rees HSP cloud research session: prio3

- Session: `session_01B1JoCj7cgT6oZy4a3Z56bG` (Claude Code cloud session)
- Started: 2026-11-04T05:01Z; final result event: 2026-11-04T05:19Z
- Task: Deeper literature-priority search (round 3) for the Rees HSP result; novelty_established stays false.
- Harvested 2026-11-05 from the session's single `result` event via the claude.ai events API.
  Body below is verbatim (SHA-256 of body: `073f365617e912f0d3ae930fa349f350fe173425f0a7342bca459e49c4246895`, 16265 chars).
- Status: AI-generated, AI-checked only, pending human review. All Rees claim gates stay false.
- Comparison with the paper: `2026-11-04-rees-cloud-research-harvest.md`.

---

# Literature-priority search, round 3: the Rees hidden-subgroup claim (2026-11-04)

Read-only search. Nothing was committed or pushed, and no one was contacted. Scratch downloads are in `/tmp/claude-0/-home-user-qsearch/10959b44-2ef0-5e02-ab40-66d215639a01/scratchpad/`. `novelty_established` stays **false**: a missing hit is not evidence of novelty.

## 0. Bottom line

**No covering result found. Prior work covers parts of it.** In arXiv, Semantic Scholar and partial Google Scholar coverage up to 2026-11-04, I found no paper that handles an arbitrary hidden subgroup H in p-groups of fixed class c ≥ 3 with p unbounded. Three 2026 papers describe the field the same way: Morales (arXiv:2608.05321, Sep 2026), Boucher–Fouque–Shen (arXiv:2609.34996, Sep 2026) and the Dutto et al. survey (arXiv:2512.02087, Dec 2025). Each names Imran–Ivanyos (bounded primes) and Ivanyos–Sanselme–Santha (class 2) as the frontier for nilpotent groups. None cites a large-p result for class ≥ 3.

The search has gaps. Google Scholar "cited by" pages hit a CAPTCHA, DBLP blocked bot access, OpenAlex ran out of free quota, and the IACR survey PDF returned 403. See §3.

Closest prior work for each ingredient:

| Ingredient | Closest prior work | Gap |
|---|---|---|
| **A1**: Rees cover R₊(L), tuple oracle, graded dilations | Ivanyos–Sanselme–Santha 0707.1260 §4: automorphisms φⱼ of exponent-p class-2 groups define group actions on coset states. Imran–Ivanyos 2304.08376 (Related results) say such automorphisms "do not exist" in class > 2. | No paper found uses a Rees algebra, deformation to the associated graded, contraction, or a Lazard or BCH model in any HSP or hidden-shift setting. As far as this search reaches, A1 is the new element. |
| **A2**: central character measurements, grade by grade | ISS (QFT over a central subgroup applied to several coset superpositions). Imran–Ivanyos (iterating down a central series by "subgroup state conversion"). | Both go down a central series. The grade-by-grade version on R₊ is new only in combination with A1. |
| **A3**: controlled right action cancelling characters via Σ sᵢᵈλᵢ = 0 | ISS Thm 3–5 (homogeneous system of d quadratic and d linear equations, Thm 5). Ivanyos–Santha 1503.09016 Thm 5 / Prop 7 (HSP → hidden polynomial graph problem, solved through diagonal systems). Decker–Høyer–Ivanyos–Santha 1305.1543. | Same mechanism (choose scalars so the characters' phases cancel), but used only for class 2 or for F_p ⋉ F_p^m with order-p subgroups. |
| **A4**: fixed-degree diagonal solver | Ivanyos–Santha 1503.09016 Thm 3 (TCS 2017), the tool itself. | The claim uses it as a black box. Expert should check the size condition n > d^{d log d}(m+1)^{d log d} (§5). |
| **A5**: abelian Fourier sampling at grade one | Standard (Kitaev/Shor). Exact version: Imran–Ivanyos 2202.04047. | None. |

## 1. Sources actually opened

"Full text" means the PDF was converted with pdftotext and searched for terms, with the cited passages read in context. It does not mean every proof was read line by line.

| arXiv id | Paper | How read | Theorems / sections checked |
|---|---|---|---|
| 2304.08376 | Imran–Ivanyos, *Zero sum subsequences and hidden subgroups* (QIP 2024) | Full text | Thm 1; "Related results"; Prop 1 (mentioned); Concluding remarks |
| 1503.09016 | Ivanyos–Santha, *Solving systems of diagonal polynomial equations over finite fields* | Full text | Thm 3, Thm 5, Cor 6, Prop 7, Cor 8, and the text before Prop 7 defining the family of subgroups |
| 0707.1260 | Ivanyos–Sanselme–Santha, *nil-2 groups* | Full text | Thm 1, Thm 2 (classical reduction for constant class), Cor 1, Prop 1, Thm 3–5 |
| 1305.1543 | Decker–Høyer–Ivanyos–Santha, *bivariate hidden polynomial* | Full text, term search | Thm 1–3, Cor 4 (constant m, r, D) |
| quant-ph/0211091 | Friedl–Ivanyos–Magniez–Santha–Sen | Full text, term search | Intro; Thm 4.16 (smoothly solvable groups: derived-series factors of bounded exponent) |
| 2202.04047 | Imran–Ivanyos, exact abelian HSP | Abstract and header | n/a |
| 2608.05321 | Morales, *HSP in Semidirect Products and Quasi-Hamiltonian Groups* (Aug/Sep 2026) | Full text, term search | Intro p.2, Fig. 1, appendix "Comparison with bounded nilpotency class" |
| 2609.34996 | Boucher–Fouque–Shen, *Cyclotomic Cosets* (Sep 2026) | Full text, term search | Intro; §1.1, which restates Imran–Ivanyos Thm 1 |
| 2609.38085 | Holt–Subramanian, *Learning quantum symmetries* (Sep 2026) | Abstract and term search | Cor 2.5, Thm 7.1, Cor 7.2–7.12. Normal hidden subgroups, StateHSP. |
| 2512.02087 | Dutto–Mercuri–Murru–Romano, HSP survey (Dec 2025) | Abstract and term search | Nilpotent paragraphs (cites ISS, II, IS only) |
| 2610.28368 | Imran, hidden parabolic subgroups over chain rings (Oct 2026) | Abstract | n/a |
| 2608.30340 | Imran, *Exact quantum splitting…* (Aug 2026) | Abstract | n/a (no HSP) |
| 2511.19494 | Dong–Fan–Zhong–Qiu, generating nilpotent groups (Nov 2025) | Abstract and term search | Sampling bounds only |
| 2507.18499 | Kuperberg, *HSP for infinite groups* (Jul 2025) | Abstract and term search | No nilpotent content |
| 2204.03295 | H. Wang, *Polynomial-time quantum algorithm for solving the HSP* | Abstract and term search | See §4 |
| 2609.02084 | Y. Wang, quantum algorithm for the radical of a Lie algebra | Abstract | Real or complex Lie algebras, no HSP |
| 2610.27250, 2610.16827, 2609.10596, 2605.12615, 2604.00929, 2312.14028, 2510.10538, 2609.35656, 2410.20162, 2510.07515 | Recent HSP-adjacent papers and citers | First page plus a search for "nilpoten" | None treats nilpotent HSP with large p |
| IACR ePrint 2026/2678 | *From Quantum Mechanics to the Hidden…* (survey) | Abstract only (PDF 403) | Abstract claims no new results |

## 2. The three closest results

**(a) Ivanyos–Sanselme–Santha, arXiv:0707.1260 (Algorithmica 2012), Thm 1.**
Quote (abstract): "groups of nilpotency class at most 2, can be solved efficiently by a quantum procedure".
Paraphrase: arbitrary H, any primes (p may grow), black-box groups of class ≤ 2. Thm 2 reduces any fixed class c to exponent-p p-groups with |H| ≤ p. The class-2 quantum step uses automorphisms φⱼ plus a quadratic-and-linear system (Thm 5).
Gap: class 2 only. The authors say the reduction "might be useful" for higher class but give no algorithm there. The claimed result is exactly a class-c version of the quantum step.

**(b) Imran–Ivanyos, arXiv:2304.08376 (QIP 23:14, 2024), Thm 1.**
Quote: "the prime factors of |G| are also bounded by a constant".
Paraphrase: an exact algorithm for arbitrary H in black-box nilpotent groups of constant class, poly(ℓ) time, conditional on finding zero-sum subsequences in F_p^n. That subroutine is only available for p = O(1). Their concluding remarks leave even smooth |G| open.
Gap: p is bounded, whereas the claim has p unbounded. Their related-work paragraph also says that, for higher class, the large-p results [DHIS14, IS17] cover only groups "with an abelian factor group of restricted kind (e.g., cyclic)".

**(c) Ivanyos–Santha, arXiv:1503.09016 (TCS 657, 2017), Cor 8.**
Quote: "If the nilpotency class of the group G of the form F_p ⋉ F_p^m is constant".
Paraphrase: quantum polynomial time for HSP(G, ℋ), where ℋ is the family of order-p subgroups not contained in 0 × F_p^m. The route is Prop 7 (reduction to a hidden polynomial graph problem), then Thm 5 and Thm 3 (diagonal systems).
Gap: one special family of groups and order-p subgroups only. It is still the closest precedent for A3/A4: diagonal-equation solving to cancel phases at unbounded p and class > 2.

Supporting evidence on the state of the art, from the most recent relevant paper found: Morales (2608.05321 v2, 28 Sep 2026) describes [II] as "efficient if the prime factors of the order are bounded by a constant". It cites nothing beyond ISS and II for nilpotent groups.

## 3. Query log (all on 2026-11-04)

"Relevant" means a result bearing on nilpotent or p-group HSP beyond background. "New" means not among the five already-known papers.

**WebSearch tool** (mode in brackets):

| # | Query | Relevant / new |
|---|---|---|
| W1 | hidden subgroup problem nilpotent group quantum algorithm 2025 [ext] | 3 / 1 (2608.05321) |
| W2 | hidden subgroup problem p-groups large prime nilpotency class three quantum polynomial time [ext] | 3 / 1 (same) |
| W3 | quantum algorithm hidden subgroup Lazard correspondence Baker-Campbell-Hausdorff [ext] | 0 (only the classical effective-Lazard paper) |
| W4 | Imran Ivanyos "hidden subgroup" … 2304.08376 cited by [std] | 0 new |
| W5 | "hidden subgroup" "Rees algebra" OR "associated graded" OR "contraction" Lie algebra quantum algorithm [ext] | 0 |
| W6 | quantum algorithm diagonal equations cancel phases hidden subgroup Chevalley-Warning [ext] | 3 known / 0 new |
| W7 | Ivanyos Santha "diagonal polynomial equations" hidden subgroup cited 2024 2025 2026 [std] | 0 new |
| W8 | hidden subgroup problem groups of nilpotency class 3 unbounded prime quantum arXiv 2026 [ext] | 1 (2608.05321) |
| W9 | "hidden subgroup" Heisenberg group Z_p^n large p quantum algorithm 2024 OR 2025 OR 2026 [std] | 0 recent (all 2005–08) |
| W10 | Ivanyos Santha 2025 2026 talk hidden subgroup nilpotent groups large primes [ext] | 0 (IACR survey) |
| W11 | QIP 2026 accepted talks hidden subgroup nilpotent [std] | 0 (programme not surfaced) |
| W12 | "hidden subgroup" "class at most p-1" OR "class less than p" quantum Lie ring [std] | 0 |
| W13 | quantum algorithm hidden subgroup "unitriangular" OR "unipotent group" finite field [std] | 0 covering (1406.6511, parabolic) |
| W14 | hidden subgroup nilpotent Kuperberg Regev Childs van Dam 2025 … [std] | 0 |
| W15 | "Dixmier" "Lister" characteristically nilpotent Lie algebra quantum algorithm [std] | 0 |
| W16 | classical query complexity hidden subgroup problem p-groups nilpotent lower bound [std] | 0 specific (context: 2107.02987, 2110.00827) |
| W17 | "hidden subgroup" "p-groups of class" OR "nilpotent Lie algebra" … F_p [ext] | 0 |
| W18 | TQC 2026 OR TQC 2025 accepted papers hidden subgroup nilpotent p-group [std] | 0 (programme not surfaced) |
| W19 | Hefeng Wang "Polynomial-time quantum algorithm for solving the HSP" … [std] | 1 (see §4) |

**arXiv search** (arxiv.org/search, abstract field unless noted, newest first; total hits in brackets):
- "hidden subgroup" nilpotent [7]: 4 relevant, 1 new (2608.05321)
- "hidden subgroup" p-groups [16]: 0 new
- Heisenberg [5]: all ≤ 2008. extraspecial [2]: known.
- Zero hits for each of: unipotent, Lazard, "Lie algebra", "Lie ring", graded, "diagonal equations", "hidden shift" nilpotent, Campbell, Malcev, unitriangular, "class three", pinching, dilations, "hidden shift" "polynomial equations", quantum "nilpotent Lie algebra" finite field, quantum algorithm "Lie algebra contraction", and (all fields) "nilpotent groups" "large primes".
- "nilpotency class" [3]: known. "Chevalley-Warning" [1]: ISS. "hidden polynomial" quantum [5]: known line. "zero sum" [1]. automorphisms nilpotent [2]. "solvable groups" [4]: known.
- quantum "Rees algebra" [4]: all off-topic (algebraic geometry, Hopf algebras).
- "coset states" nilpotent OR "p-group" [15]: none covering.
- "black-box group" nilpotent [1]: 1305.1327, off-topic.
- "hidden subgroup", all papers, newest 70 of 172: every 2023–2026 entry screened by title; 20 opened (§1).
- Author listings checked for nilpotent HSP: Ivanyos (47), Santha (70), Imran M. (quantum entries), Magniez, Kuperberg, Childs, van Dam, Regev, Sen. Zero hits.

**Citation engines:**
- Semantic Scholar API. Citers of 2304.08376: 9, all 2025–26, all screened. 1503.09016: 6. 0707.1260: about 45. 1305.1543: 4. quant-ph/0211091: 31. No covering citer.
- Google Scholar. A topic query returned 10 results, nothing new. Title pages show "Cited by 14" for both 2304.08376 and 1503.09016, but the cited-by lists were **blocked by CAPTCHA**. Up to about 5 citers of each paper are therefore unseen.
- OpenAlex. The TCS version of Ivanyos–Santha has cited_by_count 3. Further queries were refused: the free quota was exhausted, and the offered fix of registering an API key with the user's email was declined as outreach.
- DBLP (web and API) blocked by bot protection.
- arXiv export API rate-limited ("Rate exceeded"). Its first query matched the web-search result.

## 4. Flags: anything suggesting the claim is false or already known

1. **Not "already known", but a general claim exists.** H. Wang, arXiv:2204.03295 (v5, May 2023) claims a polynomial-time quantum algorithm for the general HSP, via "multistep quantum computation". It would formally cover everything. I found no journal version, and the field's 2025–26 literature treats non-abelian HSP as open (the Dutto et al. survey, Morales). I don't regard it as credible prior art. The expert may still want to decide whether it needs a sentence.
2. **No sign that the claim is false.** But one passage targets exactly A1. Imran–Ivanyos write that automorphisms useful for "twists" "do not exist in general nilpotent groups of class greater than two". A1's answer is to move to R₊(L), which is always positively graded, and use its dilations t ↦ st rather than automorphisms of G.
   - A quick consistency check found no obstruction. Evaluation at t = a is a Lie homomorphism R₊(L) → L, and via Lazard a group homomorphism, since the class of R₊ is ≤ c < p. With c distinct nonzero aᵢ, the Vandermonde matrix (aᵢᵏ), k = 1..c, is invertible, so the tuple map is injective.
   - This is my own check, not a literature finding. It is the step the expert should verify first.
3. **Scope reminder.** The condition c < p excludes 2-groups, including the dihedral D_{2ⁿ}. Morales notes that an efficient general nilpotent HSP algorithm would solve those. The claimed result therefore does not touch the dihedral or hidden-shift hardness line. Related-work text should not suggest otherwise.

## 5. What a human expert should still check

1. **The unseen citers.** Open the blocked Google Scholar cited-by lists for 2304.08376 and 1503.09016 (14 each), plus DBLP for Ivanyos, Santha and Imran for 2024–26 conference-only papers (STACS, MFCS, ISSAC, TQC). Also check the QIP 2025/2026 and TQC 2025/2026 programmes, which my searches never surfaced.
2. **Whether the access models match.** Prior work uses black-box groups with unique encoding, while the claim takes structure constants of the Lazard algebra. Decide whether the comparison is fair: can a black-box p-group of class c < p be converted to its Lazard algebra in quantum polynomial time for fixed c? If not, the result is stated in a stronger input model.
3. **The A4 parameter regime.** Ivanyos–Santha Thm 3 needs n > d^{d log d}(m+1)^{d log d} variables for m equations of degree d. Check that d ≤ c, that the number of dilation scalars used per grade meets this bound, and that the solution's nonzero or nondegeneracy conditions are what A3 needs. Thm 3 gives a nontrivial solution, not necessarily one with all sᵢ ≠ 0.
4. **The A1 recovery step** (§4.2): that the tuple oracle on R₊(L) can be built from f with O(c) queries, and that H is recovered exactly as ev_a of the hidden subgroup in R₊(L), including for non-normal H and for non-gradable L such as Dixmier–Lister.
5. **Folklore.** Ask whether "Rees or graded deformation + dilation twists" is known informally in the Ivanyos–Santha group, for instance from talks. The ISS remark that the reduction "might be useful" for higher class shows they were looking at this problem.
6. **Follow-up of the IS17 open problem.** Confirm with someone in that community that nothing after 2017 extends Cor 8 to arbitrary H. My search found none.

Main URLs: [2304.08376](https://arxiv.org/abs/2304.08376), [1503.09016](https://arxiv.org/abs/1503.09016), [0707.1260](https://arxiv.org/abs/0707.1260), [1305.1543](https://arxiv.org/abs/1305.1543), [quant-ph/0211091](https://arxiv.org/abs/quant-ph/0211091), [2608.05321](https://arxiv.org/abs/2608.05321), [2609.34996](https://arxiv.org/abs/2609.34996), [2609.38085](https://arxiv.org/abs/2609.38085), [2512.02087](https://arxiv.org/abs/2512.02087), [2204.03295](https://arxiv.org/abs/2204.03295), [2507.18499](https://arxiv.org/abs/2507.18499), [IACR 2026/2678](https://eprint.iacr.org/2026/2678).
