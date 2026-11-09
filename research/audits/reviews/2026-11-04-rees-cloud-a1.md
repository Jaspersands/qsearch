# Rees HSP cloud research session: a1

- Session: `session_01B1JoCfZNsKGrJofznH8ixw` (Claude Code cloud session)
- Started: 2026-11-03T22:54Z; final result event: 2026-11-03T23:14Z
- Task: Novelty claim A1: read the Google Scholar citers of Imran-Ivanyos (2304.08376) and Ivanyos-Santha (1503.09016).
- Harvested 2026-11-05 from the session's single `result` event via the claude.ai events API.
  Body below is verbatim (SHA-256 of body: `dfbfd7af6fd767233fbce8f8a2891c8b15eb88789b05b38738cad90c4d176aff`, 12026 chars).
- Status: AI-generated, AI-checked only, pending human review. All Rees claim gates stay false.
- Comparison with the paper: `2026-11-04-rees-cloud-research-harvest.md`.

---

I found no paper that anticipates the graded-cover algorithm for arbitrary H. Every citer of both papers that I could open treats a different regime, and searching for the idea directly also came up empty. Nothing was written inside the repository; all downloads and scripts are in the scratchpad.

**Sources and access**
- **Google Scholar:** served the citing lists from this machine with no CAPTCHA (2 pages each, about 12 s between requests). DBLP showed an anti-bot challenge, and so did CORE's web search; I did not bypass either.
- **Semantic Scholar:** worked, after one 429 retry.
- **Crossref:** counts only (cited-by needs member credentials): Imran–Ivanyos (II24) 1, Ivanyos–Santha (IS17) 2.
- **OpenAlex:** gave counts of 1 and 3, then its free daily budget for this IP ran out before the citing lists loaded.
- **Dimensions:** free metrics endpoint, counts only: 3 and 4.
- **Lens, CORE API:** both need an API key, so not queried.

**Correction to the brief:** arXiv:2304.08376 (QIP 23:14, 2024) is titled "Zero sum subsequences and hidden subgroups". "Efficient quantum algorithms for some instances of the semidirect discrete logarithm problem" is a different Imran–Ivanyos paper (Designs, Codes and Cryptography 2024, Scholar cluster 10878821474178885634, 12 citations), which I did not check. The TCS version of Ivanyos–Santha drops the "On": "Solving systems of diagonal polynomial equations over finite fields", DOI 10.1016/j.tcs.2016.04.045.

## 1. Citers of Imran–Ivanyos (Scholar shows 14 entries, which are 13 distinct works)

"Scholar" = found in cluster 9212012140591805150; "S2" = Semantic Scholar. "No" = does not give a fixed-class, growing-p, arbitrary-H HSP algorithm with a graded or Rees cover.

| # | ID | Title | Authors | Found via | Covers? Quote |
|---|---|---|---|---|---|
| 1 | arXiv 2510.07515 (also STOC 2026, DOI 10.1145/3798129.3800731; 2 Scholar entries) | No exponential quantum speedup for SIS∞ anymore | Kothari, O'Donnell, Wu | Scholar, S2 | No. Classical SIS∞ algorithm. p.4: "this easier proof is based on a method of Imran and Ivanyos [II24], but improves upon it by allowing exponentially large q." |
| 2 | 2607.14650 | Worst-Case Quantum Algorithm for Optimal Polynomial Intersection Beyond Decoded Quantum Interferometry | Horinaga, Yamakawa | Scholar | No. Optimal polynomial intersection (OPI). p.15: "Kothari, O'Donnell, and Wu [KOW26], building on earlier works [ISS12, II24]…" |
| 3 | 2512.02087 | A survey about Hidden Subgroup Problem from a mathematical and cryptographic perspective | Dutto, Mercuri, Murru, Romano | Scholar, S2 | No. Survey. p.39: "…nilpotent groups with constant nilpotency class and whose order only have prime factors also bounded by a constant [34]." |
| 4 | 2609.34996 | Cyclotomic Cosets: Hidden Subgroup and Quantum Sieving Algorithm for Prime-Power Moduli | Boucher, Fouque, Shen | Scholar, S2 | No. One specific cyclotomic group, fixed p, class t(p−1) growing; sieve. §4 p.16: "In this setting, the nilpotency class of the cyclotomic group is no longer constant." |
| 5 | 2608.05321 | The Hidden Subgroup Problem in Semidirect Products and Quasi-Hamiltonian Groups | Morales | Scholar, S2 | No. A ⋊ Z_{p^k} with scalar action, and quasi-Hamiltonian groups (every subgroup permutable, class unbounded). App. A.3 p.34: "[20] … bounded by constants. We show below that the groups studied in this paper have unbounded nilpotency class." |
| 6 | 2610.00502 | Quantum Algorithms for OPI Variants Beyond Locality and Classical Decodability | Ragavan, Shutty | Scholar | No. p.4: "…have been matched by classical algorithms [ISS12, IS15, II24, KOW25, SMR+26]." |
| 7 | 2609.40321 | Exponential quantum speedup for F₃ⁿ-Subset-Sum? Or, rigorous classical algorithms for Binary-Error LWE | Kothari, Metger, O'Donnell, Shutty, Wu | Scholar | No. p.7: "previous algorithms require n^{O(q log q)} vectors [IS17, II24]." Its "associated graded ring" (Gröbner/Hilbert series) has nothing to do with groups. |
| 8 | 2609.38085 | Learning quantum symmetries | Holt, Subramanian | Scholar, S2 | No. StateHSP. p.3: "many important families of non-abelian groups do admit efficient quantum algorithms [RB98; Gav04; GP11; ISS12; II24]." |
| 9 | 2608.30340 | Exact quantum splitting and the structure of finite algebras | Imran | Scholar, S2 | No. Finite algebras. §6.2 p.12: "Earlier applications of exact amplification to hidden-subgroup problems [17, 18] likewise motivate the exactness model…" |
| 10 | ePrint 2026/2083 | Two-Bit Lifting for Ternary SIS: Polynomial-Time Collision Attacks on LtHash | Ding, Gong, Jiang, Tang | Scholar | Almost certainly no, but **only the abstract was read**: the PDF is behind Cloudflare (403). The abstract is a ternary-SIS/LtHash collision attack (Regev–CLZ improvement) and mentions no HSP or nilpotent groups. |
| 11 | 2610.28368 | Hidden parabolic subgroups of GL_n over finite chain rings | Imran | Scholar, S2 | No. Parabolic subgroups of GL_n. p.1: "Efficient algorithms are known for selected group families [IMS01, ISS07, ISS12, II22, II24]…" |
| 12 | VUB PhD thesis 2024 | A mathematical approach to post-quantum cryptography | Carlo Emerencia | Scholar | **Full text not read**: the VUB PDF is behind Cloudflare (403). The portal abstract: "The semidirect product case has been solved for certain specific instances, but not in general", with reductions to abelian, Hamiltonian and semidirect cases. Low risk, but unverified. |
| 13 | BME PhD thesis 2024 | The Hidden Subgroup Problem and Quantum Cryptanalysis | Muhammad Imran | Scholar | No, and it explicitly leaves growing p open. Thm 3.1 p.42 requires class and prime factors bounded by constants. §3.5 p.55: "We propose the question of the existence of a poly(np)-time algorithm for finding zero-sum subsequences … A positive answer would imply … the case when \|G\| is smooth." |
| 14 | 2610.01902 | Exponential quantum advantages for decoded quantum interferometry in the streaming setting | Kewen Wu, Guangxu Yang | **S2 only** | No. p.6: "building in part on earlier classical zero-sum algorithms of Imran and Ivanyos [II24]." |
| 15 | 2510.07872 | Learning T-conjugated stabilizers: The multiple-squares dihedral StateHSP | Gideon Lee, Gross, Fukami, Jiang | **S2 only** | No. D₄ᴺ, a class-2 2-group. p.1: "some non-abelian groups have also been tackled (see e.g. Refs. [4–12])." |

Semantic Scholar names the first author of 2510.07872 "Gi-dae Lee"; arXiv gives "Gideon Lee", which I used.

**Possible extra citer, unconfirmed:** ePrint 2026/2678, "From Quantum Mechanics to the Hidden Subgroup Problem: an Overview from Finite to Infinite Groups" (Di Concilio, Flores, Kahrobaei, Noce; received 2026-10-29). It is a survey; its PDF returns 403, so I could not check whether it cites II24.

## 2. Citers of Ivanyos–Santha (Scholar cluster 8273211805831470948 shows 14 entries, which are 13 distinct works)

| ID | Title / authors | Found via | Covers? |
|---|---|---|---|
| 1712.07211 | Fast Quantum Algorithm for Solving Multivariate Quadratic Equations, Faugère et al. | Scholar, S2 | No. Quantum MQ solving; IS17 is reference 26, and I found no in-text use. |
| MDPI Mathematics 9(24):3299 (2 Scholar entries) | Transformation Method for Solving System of Boolean Algebraic Equations, Barotov et al. | Scholar, S2 | No. Boolean equations; reference-list mention only. |
| 2510.07515 | the SIS∞ paper (row 1 above) | Scholar, S2 | No. |
| 2510.06848 | Reconquering Bell sampling on qudits…, Allcock, Doriguello, Ivanyos, Santha | Scholar | No. Stabilizer learning: "techniques from hidden polynomial problems [DHIS14, IS17]." |
| 2405.06357 | Beyond Bell sampling…, the same authors | Scholar | No. Same use. |
| JCSS 2015, arXiv 1307.6429 | Generalized Wong sequences…, Ivanyos, Karpinski, Qiao, Santha | Scholar | **Looks spurious.** Neither arXiv v2 nor the 34 JCSS references in Crossref contain IS17. |
| QIP 2024, 2304.08376 | Imran–Ivanyos itself | Scholar, S2 | It is the baseline, not a rival; p.4 says [DHIS14, IS17] need "a normal subgroup with an abelian factor group of restricted kind (e.g., cyclic)." |
| 2610.00502, 2609.40321 | rows 6 and 7 above | Scholar | No. |
| SODA 2025, 2410.20162 | Solving Polynomial Equations Over Finite Fields, Dell, Haak, Kallmayer, Wennmann | Scholar, S2 | No. Classical: "Ivanyos and Santha [22] gave a polynomial-time algorithm in a restricted setting." |
| BME thesis 2024 | Imran (row 13 above) | Scholar | No. |
| ERCIM News 112 (2018) | Chevalley–Warning Theorem in Quantum Computing, Ivanyos, Rónyai | Scholar | No. One-page overview. |
| ResearchGate PDF, undated | The Journey of Quantum Information Technology, Nikolov, Galabov | Scholar | **Not read**: ResearchGate blocked the download. It looks like a general overview. |

IS17's own HSP result covers "certain semidirect product p-groups of constant nilpotency class" (its abstract), meaning groups with a cyclic or restricted abelian top. That is not arbitrary H in a general class-c group.

## 3. Searching for the idea directly
- **arXiv abstracts:** "hidden subgroup" combined with each of Lazard, Rees, graded, "Lie algebra", "Lie ring", Baker, deformation and dilation gave **0** hits. "Lower central" and "Lazard correspondence" (searched over all fields) also gave 0.
- **arXiv, other combinations:** "hidden subgroup" with nilpotent, "nilpotency class" or p-group returned only already-known papers (ISS07/12, IS15, II24, Morales) and the unrelated 2511.19494 and 1305.1327.
- **arXiv, newest HSP listings:** I also screened 2610.27250 (metabelian conjugacy), 2610.16827, 2605.12615 and 2507.18499. None cites II24 or uses any graded construction.
- **Scholar full text:** "hidden subgroup" with "Lazard correspondence", with "Rees algebra", with "associated graded" plus nilpotent, with Lazard plus nilpotent, and with "Lie ring" plus "p-group" all "did not match any articles".
- **Scholar near-misses:** the few hits on the Rees, BCH, graded-Lie and dilation queries were unrelated:
  - Ivanyos's 2007 DSc thesis ("Rees" means the Holt–Rees MeatAxe, "Lazard" means D. Lazard's Hilbert-function bound);
  - Oberwolfach Report 12/2005 (Shalev on symmetric-group Fourier sampling);
  - surveys by Kahrobaei and coauthors, and Dong on semigroups.
- **Web search (2 extended queries):** nothing beyond the extraspecial, nil-2 and II24 lines.
- **DBLP:** not searched, because of the anti-bot challenge.

## Verdict
No citer of either paper, and nothing from the independent searches, gives a quantum HSP algorithm for class-c groups with p growing and arbitrary H via ⊕ tᵏγ_k(L) or any graded substitute.
- **Closest prior art:** II24 and Imran's thesis cover constant p only. The thesis (§3.5, p.55) states that the growing- and smooth-p case is open.
- **Next closest:** Morales (quasi-Hamiltonian groups, permutable subgroups only) and Boucher–Fouque–Shen (fixed p, one group, growing class).

**Still unresolved:** full texts of ePrint 2026/2083, the Emerencia thesis, ePrint 2026/2678 (whether it cites II24 at all) and Nikolov–Galabov. All are blocked by Cloudflare or ResearchGate. Their abstracts make anticipation very unlikely, but they are unread. To close them, open the PDFs from a browser, and rerun the OpenAlex `cites:W4390615388` and `cites:W1807692705` filters after the midnight-UTC budget reset or with a key.

The downloaded texts and scripts are in `/tmp/claude-0/-home-user-qsearch/a57ca9e6-6e15-56b4-9654-6a1349f583f4/scratchpad/pdf` and `/tmp/claude-0/-home-user-qsearch/a57ca9e6-6e15-56b4-9654-6a1349f583f4/scratchpad/dl`.

Web sources: [ePrint 2026/2678](https://eprint.iacr.org/2026/2678), [VUB thesis page](https://researchportal.vub.be/en/publications/a-mathematical-approach-to-post-quantum-cryptography/), [ePrint 2026/2083](https://eprint.iacr.org/2026/2083), [Oberwolfach 12/2005](https://ems.press/journals/owr/articles/793), [ISS07](https://www.irif.fr/~santha/Papers/iss07.pdf), [arXiv 2304.08376](https://arxiv.org/pdf/2304.08376), [arXiv 2608.05321](https://arxiv.org/abs/2608.05321).
