# Rees A1 priority, remaining gap: Imran–Ivanyos and Ivanyos–Santha citers

Date: 2026-11-02. Item 13 of `research/REES_FULL_CAMPAIGN_2.md`. Sonnet 5.5 session. Read-only on the repo; this file is the only thing written.
Raw material: `/private/tmp/claude-501/-Users-jaspersands-Developer-qsearch/9d5e25ba-b833-49b9-9326-0de5c91f0d21/scratchpad/` (`api/` = JSON dumps; `q/pdf`, `q/txt` = 127 arXiv PDFs and pdftotext output; `q/cands*.json` = candidate lists).
Labels as in the round 1 report: **FULL**, **SCAN** (keyword scan plus the passages that matched were read), **ABS**.

## 0. Bottom line

- **The four missing Imran–Ivanyos citers were not all found.** Google Scholar says 14. After the sweep I can name **12** citers of arXiv:2304.08376 / the QIP paper, each confirmed by text (11 by an index, 1 by full-text grep only). Round 1 had 10. Two are new: **2610.00502** and **2607.14650**. Three Scholar entries remain unidentified. Google Scholar "cited by" is blocked by a CAPTCHA in both browsers here (§1), and I did not try to get around it.
- **None of the new citers touches nilpotent or p-group HSP, Lazard/BCH, or graded covers.** Both are classical/quantum decoding papers that cite II24 only for classical finite-field zero-sum algorithms.
- **Ivanyos–Santha:** no new HSP-relevant citer. One new text-only citer (2610.00502). Total listed 7.
- **A1 verdict unchanged: possibly new in the stated regime**, with the coverage statement now "12 of 14 Scholar-counted Imran–Ivanyos citers read; 3 unidentified". The paper's related-work text needs one clause (§6). No other change.

## 1. Sources tried

| Source | Result |
|---|---|
| Google Scholar `cites=9212012140591805150` ("Cited by 14", cluster for the QIP/arXiv versions) | Search page works (confirms 14, abstract). The "cited by" page returns the `google.com/sorry` CAPTCHA in the built-in browser and in the user's Chrome. Not bypassed. A person has to open the link and read it: `https://scholar.google.com/scholar?cites=9212012140591805150` |
| Semantic Scholar Graph API (by arXiv id, by QIP DOI 10.1007/s11128-023-04228-2) | 9 citers (same list both ways) |
| OpenAlex (W4390615388 = QIP version) | 1 citer (the ACM SIS∞ paper, 10.1145/3798129.3800731, which is 2510.07515's published form) |
| **INSPIRE-HEP** (recid 2651959; new source) | **10 citers**: the S2 nine minus 2512.02087 (survey), plus 2609.40321 and 2610.00502 |
| OpenCitations (DOI) | 1 citer (2512.02087) |
| Crossref | `is-referenced-by-count` = 1 |
| arXiv API, 29 field-restricted queries (HSP, nilpotent, p-group, semidirect, solvable, zero-sum, SIS, DQI, OPI, Regev reduction, hidden shift, StateHSP, …), 2023+ results only; downloaded 127 PDFs and grepped for `Imran`, "Zero sum subsequences", `Ivanyos and Santha`, "diagonal polynomial" | Found **2607.14650** (in no index) and confirmed every indexed citer. Hits that were *not* citers: 2512.22959 and 2510.06097 (see §3) |
| arXiv full-text search | Not available (arXiv has no full-text search; the API is metadata only). The PDF grep above is the substitute and covers only the 127 candidates |
| DBLP | Bot-challenge page. Not obtained |
| WebSearch (3 queries incl. one extended) | Only the paper's own pages and the already known citers |
| ePrint 2026/2678 (Di Concilio–Flores–Kahrobaei–Noce, HSP survey) | Abstract page read (browser). The PDF is behind a Cloudflare challenge; not bypassed. **Unread.** It is a survey and a plausible Scholar citer |
| ePrint 2026/2249 | Same Cloudflare block; it is the IACR copy of 2609.34996, which counts once |

## 2. Full citer lists

### 2.1 Imran–Ivanyos, arXiv:2304.08376 = QIP 23(1):14 (2024). Scholar 14; identified 12

| # | Paper | Found by | Read |
|---|---|---|---|
| 1 | 2510.07515 Kothari–O'Donnell–Wu, SIS∞ | S2, OpenAlex, INSPIRE | FULL §5.2 (round 1) |
| 2 | 2510.07872 multiple-squares dihedral StateHSP | S2, INSPIRE | SCAN (round 1); this session: ref [5] only |
| 3 | 2512.02087 HSP survey | S2, OpenCitations (not INSPIRE) | FULL nilpotent sections (round 1) |
| 4 | 2608.05321 Morales, semidirect/quasi-Hamiltonian | S2, INSPIRE | FULL (round 1) |
| 5 | 2608.30340 exact quantum splitting of finite algebras | S2, INSPIRE | SCAN (round 1) |
| 6 | 2609.34996 Cyclotomic Cosets | S2, INSPIRE | FULL (round 1) |
| 7 | 2609.38085 Holt–Subramanian / "Learning quantum symmetries" | S2, INSPIRE | FULL (round 1); lines 149, 460: II24 in a list of "efficient algorithms for specific families" |
| 8 | 2610.01902 DQI streaming | S2, INSPIRE | SCAN (round 1) |
| 9 | 2610.28368 hidden parabolic subgroups over chain rings (author: Imran, so a self-citation) | S2, INSPIRE | FULL abstract/intro (round 1); line 35: II24 in a list of families with known efficient algorithms |
| 10 | 2609.40321 F_3^n-Subset-Sum | not in S2/OpenAlex lists for II24, **but INSPIRE lists it** | FULL §1.3 (round 1) |
| 11 | **2610.00502** Ragavan–Shutty, "Quantum Algorithms for OPI Variants Beyond Locality and Classical Decodability" | **INSPIRE only** (new) | SCAN; lines 367–371 and the reference list read, §5.2 passage read |
| 12 | **2607.14650** Horinaga–Yamakawa, "Worst-Case Quantum Algorithm for Optimal Polynomial Intersection Beyond DQI" | **PDF grep only; in none of S2/OpenAlex/INSPIRE** (new) | SCAN; line 786 and reference read |
| — | 3 further Scholar entries | unidentified | — |

Round 1 listed 10 (rows 1–9 plus 2609.40321, which it found by text). Rows 11 and 12 are new, so 12 of Scholar's 14 are accounted for if Scholar counts both; this leaves 2 to 3 unidentified, depending on whether Scholar counts the ePrint copy of 2609.34996 separately.

### 2.2 Ivanyos–Santha, arXiv:1503.09016 = TCS 657 (2017) 73–85, DOI 10.1016/j.tcs.2016.04.045; FAW 2015 version DOI 10.1007/978-3-319-19647-3_12. Listed 7

| # | Paper | Found by |
|---|---|---|
| 1 | 1712.07211 Fast quantum algorithm for MQ | S2, OpenAlex, INSPIRE |
| 2 | 2304.08376 Imran–Ivanyos | S2, OpenAlex, INSPIRE |
| 3 | 2410.20162 / SODA 2025 "Solving polynomial equations over finite fields" | S2 |
| 4 | 2510.07515 KOW (SIS∞) | S2; PDF grep (5 hits) |
| 5 | 2609.40321 F_3^n-Subset-Sum | S2, INSPIRE |
| 6 | Math. 9(24):3299 (2021), Boolean equations transformation | S2, OpenAlex |
| 7 | **2610.00502** Ragavan–Shutty | INSPIRE; PDF (ref [IS15], line 367) |

TCS DOI per OpenAlex: 4 citers on the arXiv record, 1 on the journal record (the same Boolean-equations paper's twin). The FAW record has no citers in S2. Scholar was not reachable, so I cannot give Scholar's count for these. Round 1 listed 6 (S2) / 4 (OpenAlex); the one addition is row 7.

### 2.3 Imran–Ivanyos QIP version
Same cluster as §2.1. Semantic Scholar merges the arXiv and QIP versions (9 citers either way); OpenAlex's QIP record has 1 citer; OpenCitations has 1. No QIP-only citers appeared.

## 3. Triage

| Paper | Touches nilpotent / p-group HSP, Lazard/BCH, graded cover? | Verdict |
|---|---|---|
| 2610.00502 Ragavan–Shutty (OPI, Regev reduction; Google Quantum AI/MIT) | No. 0 hits for nilpotent/Lazard/graded/p-group. Mentions "[ISS12, IS15, II24]" once as "classical algorithms for related finite-field zero-sum and polynomial-equation problems" (line 367–368) | **Does not cover A1** |
| 2607.14650 Horinaga–Yamakawa (OPI worst case; NTT) | No. 0 hits for nilpotent/Lazard/graded. II24 cited once, line 786: KOW26 "building on earlier works [ISS12, II24]" give classical algorithms in the known regime | **Does not cover A1** |
| 2512.22959 "Revisiting finite Abelian HSP…" (Qiu et al.) | Not a citer. Its "[27] Imran–Ivanyos" is the 2022 QIC paper "An exact quantum hidden subgroup algorithm and applications to solvable groups", not 2304.08376. Nilpotent hits are Sylow-factor remarks and a generation-count lemma | Not relevant |
| 2510.06097 Chailloux–Hermouet (S\|LWE⟩ vs ISIS) | Not a citer. Its "II24" is a different Imran–Ivanyos paper (semidirect discrete log, DCC 92) | Not relevant |
| 2401.06964 (moments subset sum via diagonal systems) | Not a citer of IS (0 hits for IS15/IS17/"Ivanyos and Santha" in the text) | Not relevant |
| ePrint 2026/2678 (survey) | Unknown. Abstract only | **Unread; a survey that cites II24 would at most restate it** |

Not repeated here: the 10 round-1 rows, whose table stands.

## 4. Full-text verdicts with theorem numbers

- 2610.00502 and 2607.14650: no theorem numbers to cite for A1; the II24/IS15 passages are lines 367–371 and 786 of the pdftotext output (§1 introduction/related work). Neither proves or cites a statement about nilpotent groups. 2610.00502 §5.2 cites Friedl–Ivanyos–Magniez–Santha–Sen Thm 3.5 and Ivanyos Thm 1 for Arora–Ge relinearization; this is about excluded-value constraints on linear unknowns and is not a cover.
- Labels: SCAN with the matched passages read. This is weaker than FULL, and a missing hit is not evidence of novelty; but a decoder/OPI paper has no reason to contain a nilpotent-HSP construction, and both abstracts and the sections around the citations are about code decoding.
- No theorem numbers beyond those in the round 1 table are needed.

## 5. Updated A1 verdict

**Possibly new in the stated regime.** Unchanged. The evidence base is now:
- Imran–Ivanyos citers: 12 of Scholar's 14 identified, all but the 3 unlisted read to at least the level in §2.1.
- Ivanyos–Santha citers: 7 identified; Scholar's count unavailable.
- Directly searched vocabulary (round 1 §3) plus 29 arXiv queries and a 127-paper full-text grep this session: no graded/Rees cover, dilation action or evaluation-tuple oracle for HSP anywhere.
- Gaps: 3 Scholar-only Imran–Ivanyos citers (most likely a thesis, a survey such as ePrint 2026/2678, or a non-arXiv conference paper; not established); the Wang claim arXiv:2204.03295 remains unread (still not credited by any 2026 source).

## 6. Proposed paper text

Only the coverage sentence changes. Replace the round-1 wording ("through 2026-11-02, with Scholar gaps") with:

> We are not aware of a prior construction of this kind. We checked the papers that cite Imran–Ivanyos and Ivanyos–Santha, as listed by Semantic Scholar, OpenAlex, INSPIRE-HEP and OpenCitations on 2 November 2026 together with a keyword search of the 2023–2026 arXiv literature on the hidden subgroup problem; Google Scholar lists three further citing works of Imran–Ivanyos that we could not identify.

The 2610.00502 and 2607.14650 citations need no new sentence; both support the existing remark that Imran–Ivanyos is used for classical finite-field zero-sum problems (cite [KOW26] and 2609.40321 as before).

## 7. Claim gates (must stay false)

- "No prior work exists" / "first graded cover for HSP": stays unclaimed. Three Imran–Ivanyos citers are unidentified and Ivanyos–Santha's Scholar count is unknown.
- "Covered all citing literature": must not be claimed.

## 8. Next command

A person with a browser opens `https://scholar.google.com/scholar?cites=9212012140591805150` (CAPTCHA) and pastes the 14 titles; also the Ivanyos–Santha cluster (search "Solving systems of diagonal polynomial equations over finite fields"). Acceptance test: any title not in §2.1 is read for nilpotent/Lazard/graded and added here. Also fetch ePrint 2026/2678 in a browser and grep for "Imran", "nilpotent", "Lazard".
