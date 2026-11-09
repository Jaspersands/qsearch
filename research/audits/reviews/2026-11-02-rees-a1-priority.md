# Rees A1 priority: is the positive lower-central Rees cover for arbitrary H already known?

Date: 2026-11-02. Item 1 of `research/REES_FULL_CAMPAIGN.md`. Sonnet 5.5 session. Read-only on the repo; this file is the only thing written.
Raw downloads and API dumps: `/private/tmp/claude-501/-Users-jaspersands-Developer-qsearch/56e58f7a-27a0-47cf-b5d2-8e6c180796b6/scratchpad/{cit,pdf2}/` (pdftotext of full PDFs).
Labels: **FULL** = full PDF converted to text; the sections named were read, the rest was keyword-scanned (terms: nilpotent, Lazard, p-group, Rees, dilation, graded, hidden subgroup, Ivanyos, zero-sum). **SCAN** = full text scanned by keyword only, no section read. **ABS** = abstract or snippet only (supports no verdict). A missing hit is not evidence of novelty.

A1 as tested (`main.tex` Thm `thm:rees-cover`, Lem `lem:homogeneous`, Prop `prop:single-evaluation`): the positive graded algebra A = ⊕ t^k γ_k(L) with evaluations E_s and dilations δ_λ, and the c-tuple oracle f̂(a) = (f(E_{s_1}(a)),…,f(E_{s_c}(a))), whose hidden set is the δ-stable lift of log H for ARBITRARY H, in a Lazard group of class c < p, p growing.

## 0. Bottom line

**Verdict on A1: possibly new in the stated regime (not "known", not "partly known").** I found and read the 2023–2026 citing literature, which is small. Nothing in it, and nothing from the topical searches, constructs a graded or Rees-type cover, a dilation action, or an evaluation-tuple oracle for HSP. The closest results are conceptual neighbours:
- Ivanyos–Sanselme–Santha (nil-2 automorphism twists, c = 2 only);
- Imran–Ivanyos (arbitrary H, central-series descent by zero-sum subsequences, primes bounded);
- Ivanyos–Santha Cor 8 (growing p, but only F_p ⋉ F_p^m and hidden order p outside F_p^m).

Coverage is still incomplete (§3): Google Scholar reports "Cited by 14" for Imran–Ivanyos, but I could list only 10 (Semantic Scholar 9, OpenAlex 1), and 3 of the 9 are the other session papers. For Ivanyos–Santha I listed 6 (Semantic Scholar) / 4 (OpenAlex); Scholar was not reachable. All 2026 citing papers I could list are read below. The unreachable remainder is most likely uncited-by-title surveys and theses, but this is not established.

Side findings that bear on other parts of the paper (not A1) are in §5.

## 1. Citing papers collected

Sources: Semantic Scholar Graph API (`/paper/arXiv:ID/citations`, complete list returned, no `next` token), OpenAlex (`cited_by_count`), and Semantic Scholar for the three neighbours (ISS `0707.1260`, DHIS `1305.1543`, IMS `quant-ph/0102014`; the last has 118 citing records, mostly 2000–2008 generic HSP). Google Scholar page fetch returned only "Cited by 14" without titles.

**Cite 1503.09016 (Ivanyos–Santha): 6 (S2); 4 (OpenAlex).**
2609.40321 (F_3^n subset sum), 2510.07515 (Kothari–O'Donnell–Wu, SIS∞), 2410.20162 (polynomial equations over finite fields), 2304.08376 (Imran–Ivanyos), a 2021 Boolean-equations paper (no arXiv id; not obtainable, title irrelevant), 1712.07211 (MQ quantum algorithm).

**Cite 2304.08376 (Imran–Ivanyos): 9 (S2); 1 (OpenAlex).**
2610.28368 (parabolic HSP over chain rings), 2610.01902 (DQI streaming), 2609.38085 (Holt–Subramanian), 2609.34996 (cyclotomic cosets), 2608.30340 (exact quantum splitting of finite algebras), 2608.05321 (Morales), 2512.02087 (HSP survey), 2510.07872 (multiple-squares dihedral), 2510.07515 (Kothari–O'Donnell–Wu).

Also cited-by-reference only (not in the S2 lists, found by scanning texts): Imran–Ivanyos is cited by 2609.40321 and 2610.01902 (text mentions) and by 2609.34996 as its main tool.

## 2. Per-candidate table

"Closest theorem" = the theorem in that paper nearest A1. "Covers A1?" is judged against the tuple-oracle/graded-cover claim for arbitrary H, class c < p, p growing.

| Reference | Read | Closest theorem | Covers A1? Why / why not |
|---|---|---|---|
| Imran–Ivanyos, arXiv:2304.08376 (QIP 23:14) | FULL: intro, Prop 1, Lemma 2, Props 2–3, §5 statements, §6 | Thm 1; Lemma 2 (zero-sum ⇒ subgroup-state conversion G → G/L, L ≅ F_p^n central); Prop 2/3; §6 | **No.** Arbitrary H, any fixed class, exact, but primes of \|G\| bounded by a constant (Thm 1); mechanism is zero-sum subsequences (binary weights), not graded evaluations. §6 poses poly(np) zero-sum as open and says a positive answer would give smooth order. Intro p. 4 says the class-2 automorphism tool "do[es] not exist in general nilpotent groups of class greater than two". The Rees dilations live on the cover A, not on G, so that remark is compatible with A1 and does not cover it. |
| Ivanyos–Santha, arXiv:1503.09016 (TCS 2017) | FULL: Thm 3, Def 4, Thm 5, Cor 6, Prop 7, Cor 8 statements; intro | Cor 8 (G = F_p ⋉ F_p^m, class constant, HSP solvable); Thm 3 (SDE solver) | **No.** Growing p, fixed class, but only one group family and a restricted family of hidden subgroups (order p, not inside 0 × F_p^m; the family is fixed in the paragraph before Prop 7). SDE solver is an ingredient for A2, not a cover. |
| Ivanyos–Sanselme–Santha, arXiv:0707.1260 (Algorithmica 2012), neighbour | FULL (prior session 11-01) | Thm 1, Prop 1, Lemma 5, Thm 5 | **No.** Class 2 only; φ_j automorphism twists with a quadratic-plus-linear system. Overlap in spirit (scalar weights j, j²), not in construction. |
| Cyclotomic Cosets, arXiv:2609.34996 | FULL: §1, Lemma 2 statement, §4 (Thm 1 quote of II, Lemma 6–7, Thm 2 quote, Thm 3) | Thm 3 (quasi-poly CCP solver); Lemma 6 (PSP level reduction) | **No.** Group R_q^n ⋊ F_p, class t(p−1) (not < p), hidden subgroups of order p, p treated as constant (equivalences "when p constant"). Uses II's zero-sum Thm 2 as a black box (p^{O(p log² p)}). A reduction of this kind uses central-series sieving, not graded evaluation. Useful as evidence that the II technique is the one people apply. |
| Morales, arXiv:2608.05321 | FULL: abstract, intro, §1 remarks on [17,20] | abstract theorems; App. A.3 | **No.** Groups A ⋊ Z_{p^k} with scalar action (bounded generator rank) and quasi-Hamiltonian groups; text says class "need not be bounded" and treats [17]=ISS (class 2) and [20]=II as the nilpotent state of the art. Nothing graded. |
| Holt–Subramanian, arXiv:2609.38085 | FULL (11-01) + scan | — | **No.** Normal H only; 0 hits for nilpotent/Lazard/graded. Zero-sum there is the coding-theory notion. |
| HSP survey, arXiv:2512.02087 | FULL: §§ on nilpotent results (≈ line 1759, 2029) | survey statements | **No.** States II as the latest nilpotent result: constant class and bounded prime factors. Confirms nothing newer as of Dec 2025. |
| Kothari–O'Donnell–Wu, arXiv:2510.07515 | FULL: §5.2 (Works by Imran, Ivanyos, Sanselme, Santha), §1 | §5.2; Thm 1.x on SIS∞ | **No.** Classical zero-sum / SDE only; §5.2 summarizes IS17 and II24 as the same line, with II24's m ≥ q^{Cq log q} n^{⌊q/2⌋⌈log₂ q⌉}. No HSP construction. |
| F_3^n-Subset-Sum, arXiv:2609.40321 | FULL: §1.3 statements (Thm 1.10, 1.11), references to IS17/II24/KOW26 | Thm 1.11 (worst-case zero-sum with m ≥ q^{q²}(n+1)^{q−1}) | **No** for A1. See §5: improves the zero-sum exponent for fixed q. "Graded ring" hits are Gröbner-basis, unrelated. |
| Hidden parabolic subgroups, arXiv:2610.28368 | FULL: abstract, intro, Thm 1.1 | Thm 1.1 | **No.** GL_n over chain rings, parabolic H; II22/II24 appear only in a list of "efficient algorithms for selected group families". |
| Exact quantum splitting, arXiv:2608.30340 | SCAN + reference list | — | **No.** Finite algebras over fields, Jacobson radical; II24 is a reference only. |
| DQI streaming, arXiv:2610.01902 | SCAN; line 296 | — | **No.** Cites II24 for classical zero-sum. |
| Multiple-squares dihedral StateHSP, arXiv:2510.07872 | SCAN | — | **No.** Dihedral; cites II24 and ISS12 in the reference list. |
| Solving polynomial equations over finite fields, arXiv:2410.20162 | SCAN | — | **No.** Cites IS17 for restricted-case SDE complexity only. |
| MQ fast quantum algorithm 1712.07211; Boolean equations 2021 | SCAN | — | **No.** Equation solving, no HSP. |
| Allcock–Doriguello–Ivanyos–Santha, arXiv:2405.06357 and 2510.06848 (cite DHIS14 / ISS12 / IS17) | SCAN | — | **No.** Stabilizer-state learning on qudits (Heisenberg-type Bell sampling); 0 nilpotent hits. |
| Abelian Hypergroups and Quantum Computation, arXiv:1509.05806 (cites ISS) | FULL: abstract, §1 contribution list | Main results IV | **No.** Hidden **normal** subgroups of nilpotent groups. Its intro says no efficient algorithm is known for nilpotent HSP. |
| Quantum polynomial-time conjugacy in metabelian groups, arXiv:2610.27250 | SCAN | — | **No.** Conjugacy in finitely generated metabelian groups; nilpotent hits are nilpotent *elements* and a TC⁰ citation. |
| Improved Quantum Algorithms for Black-Box Abelian Group Decomposition, arXiv:2609.36480; QFT toolbox 2608.28573 | SCAN | — | **No.** Abelian, or QFT circuits; no nilpotent/graded hits. |
| Polynomial-time quantum algorithm for solving the HSP, arXiv:2204.03295 (Wang) | SCAN only (0 hits for nilpotent/graded) | — | Not usable. Claims a general algorithm; no 2026 source in this audit credits it and Morales/Holt–Subramanian/Imran–Ivanyos-era surveys still call the nonabelian HSP open. I did not read the argument. |
| ePrint 2026/2678 (HSP survey) | **Not obtainable** (HTML challenge page on direct fetch; 403 earlier) | — | Unread. No verdict depends on it. |
| Others from the IMS01 / ISS12 citing lists (normalizer circuits, hypergroups, universal algebras 2001.11298, deterministic HSP 2110.00827, black-box expanded groups 2505.20497, min generating set 2609.40260, group order in QCMA, SDLP papers 2209.02814, 2312.14028, DHIS-adjacent Bell sampling) | SCAN of the downloaded ones; titles only for the rest | — | **No** by keyword scan. 2505.20497 mentions nilpotent additive groups of expanded groups (isomorphism/decidability, not HSP). 2609.40260 mentions nilpotent only in a Fitting-series subroutine. 2511.19494 (generation of nilpotent groups) gives sample counts for the abelian HSP only. |

Not read at all: Hallgren–Russell–Ta-Shma (paywalled, background only), the Google Scholar items beyond the 10 above.

## 3. Direct search for the A1 vocabulary

Rees algebra, graded Lie ring, dilation, Lazard, BCH, scalar action, unipotent, Heisenberg, hidden shift on nilpotent groups. Result: no hit connecting any of these to a quantum HSP algorithm, in five WebSearch queries, one extended-mode query, six OpenAlex keyword queries (2014–2026), and Semantic Scholar keyword searches (rate-limited, 0 results returned). Every query returns the same two nilpotent HSP sources (ISS12 and II24), plus Morales and the cyclotomic-coset paper from 2026. The Lazard correspondence appears only in classical p-group isomorphism papers (Grochow–Qiao tensor-isomorphism line, 2021–2025), which are not about HSP and use graded structures differently (not read beyond title and snippet).

## 4. Query log (all 2026-11-02)

WebSearch (standard unless noted):
1. quantum hidden subgroup problem nilpotent group Lazard correspondence Lie algebra arbitrary hidden subgroup large prime
2. "hidden subgroup" "Rees algebra" OR "Rees construction" OR "graded Lie algebra" quantum algorithm nilpotent group
3. quantum algorithm hidden subgroup p-groups nilpotency class less than p Baker-Campbell-Hausdorff
4. hidden subgroup problem nilpotent groups dilation automorphism scalar action central series quantum 2024 2025 2026
5. Imran Ivanyos "exact quantum hidden subgroup algorithm" nilpotent follow-up generalization unbounded prime
6. (extended) quantum algorithm hidden subgroup problem nilpotent group arbitrary hidden subgroup polynomial time "Lie algebra" OR "Lazard" OR "graded" OR "Rees" 2025 2026 arXiv
WebFetch: Google Scholar `scholar?cites=…` page (returned only "Cited by 14", no titles).

Semantic Scholar Graph API: citations of arXiv:1503.09016, 2304.08376, 0707.1260, 1305.1543, quant-ph/0102014 (fields title, year, externalIds). Keyword search endpoint: 7 queries, all HTTP 429 (no results).
OpenAlex API: `cited_by_count` for doi:10.48550/arxiv.1503.09016 (4) and 2304.08376 (1); keyword search (filter from 2014): "hidden subgroup problem nilpotent groups quantum algorithm", "hidden subgroup Lazard correspondence Lie algebra p-group quantum", "hidden subgroup problem Rees algebra graded dilation", "quantum algorithm p-groups nilpotency class hidden subgroup large prime", "hidden subgroup problem unipotent group finite field quantum", "hidden shift nilpotent group quantum sieve Kuperberg".
arXiv listing API (`export.arxiv.org/api/query`): 5 field-restricted queries, HTTP 429, no results.
Full-text downloads from arxiv.org/pdf (27 PDFs), plus eprint.iacr.org/2026/2678 (blocked).

Rate limits mean the keyword searches are weaker than they look. The citation lists are the strong part.

## 5. Findings that bear on other parts of the paper (not A1)

1. **Zero-sum bound improved (arXiv:2609.40321, Thm 1.11; also KOW26 = 2510.07515, §5.2).** For worst-case zero-sum in F_q^n the sequence length drops from n^{O(q log q)} to q^{q²}(n+1)^{q−1}. This is the fixed-q exponent for the *Imran–Ivanyos* route and is exponential in q, so it does not change the comparison with Rees (c-fixed degree SDE is poly(p)). Related-work text that quotes Imran–Ivanyos's S(p,n) = p^{O(p log² p)} n^{O(p log² p)} should add this improvement. It is a Related-work update only. Statement is quoted from the theorem as printed; I did not recheck its proof.
2. **Imran–Ivanyos is being used beyond constant class** (2609.34996, class t(p−1), quasi-polynomial). That paper explicitly says non-constant class and sample-only access break the exact theorem and uses II's Thm 2 as a black box. Worth a sentence in related work.
3. **Imran–Ivanyos Prop 3 (non-exact version) and §6** say a randomized or average-case zero-sum finder with poly(np) cost would give "a new result in the non-exact setting: … nilpotent groups of smooth order having O(1)-bounded nilpotency class". Rees, if correct, gets this for Lazard p-groups (class < p) by a different route. The related-work paragraph should state this sentence precisely, as the 11-01 check already proposed (its §8).

## 6. The exact statement that now holds

- *Proved by literature reading* (quantifiers: for the papers listed in §2, restricted to the full-text sections named): none of the papers that cite arXiv:1503.09016 or arXiv:2304.08376 (as listed by Semantic Scholar and OpenAlex on 2026-11-02, 10 distinct papers, all read at the level stated in the table) contains a graded/Rees cover, a dilation action, or an evaluation-tuple oracle for HSP, and none gives arbitrary H in class c < p with p growing. Access model checked: explicit group, black-box with unique encoding (II), or explicit semidirect product (IS). The closest hypotheses-weakening is Imran–Ivanyos Thm 1 (primes bounded) and Ivanyos–Santha Cor 8 (one group family).
- Not established: that no *uncited-by-these-two* paper contains the construction; that Scholar's four extra Imran–Ivanyos citations (14 vs 10) do not; Wang's arXiv:2204.03295 claim (unread).

## 7. What is still missing

1. The four Imran–Ivanyos citations Google Scholar lists beyond S2/OpenAlex, and any Ivanyos–Santha citations Scholar has. Smallest fix: a Scholar "Cited by" listing run by a person with browser access, or Semantic Scholar with an API key (rate limits blocked search endpoints). Whoever does it should read the 2024–2026 hits that mention nilpotent or Lie.
2. ePrint 2026/2678 (survey). Fetch needs a browser.
3. Expert read of Grochow–Qiao tensor-isomorphism and Lazard-based classical p-group work to confirm there is no quantum-HSP use. Titles and snippets only so far.

## 8. Claim gates that must stay false

- "A1 is new" / "first graded cover for HSP" / "the first algorithm for arbitrary H at class > 2 with growing p": must stay unclaimed. The honest statement is "we are not aware of a prior …; the closest are ISS (class 2), Imran–Ivanyos (bounded primes) and Ivanyos–Santha Cor 8 (one family)", and it should say the search covered citing papers through 2026-11-02 with the gaps in §7.
- "Imran–Ivanyos says no automorphism trick exists beyond class 2" must not be quoted as saying the Rees dilations cannot exist: their remark is about automorphisms of G, the Rees dilations are automorphisms of the cover A (and homomorphisms E_s : A → L).

## 9. Text fixes for `main.tex` (listed, not applied)

1. Related work (around line 116): add Imran–Ivanyos §6 and Prop 3 wording (§5 item 3) and the 2609.40321 / KOW26 zero-sum improvement (§5 item 1) so the bound quoted for II24 is current.
2. Where the paper cites the "do not exist in general" remark, qualify it as about automorphisms of G (II24 §1, p. 4), not of the cover.
3. State in the related-work paragraph that citing-paper coverage was through 2026-11-02, with Scholar gaps, so the priority sentence is not read as exhaustive.
4. Optionally cite 2609.34996 as an example of II24 being applied at non-constant class.
