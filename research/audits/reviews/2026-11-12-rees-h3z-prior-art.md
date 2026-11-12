# Prior-art search: HSP for arbitrary subgroups of H_3(Z) and the quadratic zero-sum problem (2026-11-12)

**Status: AI literature search by one Claude Code helper, pending human and specialist review.**
No Git commands were run, no existing file was edited, and no repository content was sent off the
machine. Only mathematical terms were used as queries. Claim gates are unchanged:
`novelty_established` stays **false** whatever this search finds, and `speedup_claim_allowed`
stays false too. Every fetched text was treated as untrusted data. Downloaded third-party PDFs and
text files are in the session scratchpad (`.../scratchpad/priorart_dl/`), not in the repo.

Local claims checked against the literature:
* **Theorem A** (`2026-11-12-rees-h3z-infinite-index.md` §2, refereed in `-h3z-referee.md` and
  `-h3z-imports.md`): the case H ∩ Z ≠ 1 is polynomial, given Kuperberg arXiv:2507.18499 Thm 1.5
  (and Thm 7.1), plus ISS 2012 and II 2023 through cor:utz.
* **Theorem C′** (`2026-11-12-rees-h3z-cyclic-proof.md` §6): the case of cyclic H with
  H ∩ Z = 1. It uses a twisted coset-state measurement, then QZS (find nonzero μ with
  ‖Σθ_iμ_i²‖ ≤ 2^{-K} and |μ| ≤ 2^{poly K}), solved by SDA-ISO, which is LLL simultaneous
  Diophantine approximation followed by a 2-D isotropic-line Gauss reduction modulo an auxiliary
  prime q (`-h3z-qzs-attack.md` §2).

## Verdict

**No prior solution was found. Some parts overlap with known work.**

1. **Main question (HSP for every subgroup of H_3(Z), including infinite index).** No paper,
   preprint, talk or survey I could open claims a quantum polynomial-time algorithm or a hardness
   result for this problem. The most recent expert statements found call it open:
   * ePrint 2026/2678 (received 29 Oct 2026), §10 item 5: "it is open whether the HSP in the
     discrete Heisenberg group H_3(Z) can be solved efficiently". It does not separate finite
     from infinite index.
   * Kuperberg's 2020 talk, final slide: "There might be a good quantum algorithm for HSP in
     nilpotent groups." This is a conjecture, not a result.

   Status: **no prior solution found (UNKNOWN whether one exists).** This search cannot rule
   out unpublished or unindexed work (see Limits).
2. **Theorem A.** Its ingredients are prior: Kuperberg Thm 1.5 for Z^k with infinite-index H,
   ISS 2012, and II 2023. The combination for H_3(Z) with H ∩ Z ≠ 1 was not found stated. The
   nearest general statement, Kuperberg Cor 1.9, gives only 2^{O(√n)} time for virtually abelian
   groups. H_3(Z) is not virtually abelian, although H_3(Z)/⟨z^r⟩ is. **Partial overlap, by
   composing prior theorems.**
3. **Theorem C′.** The template is the ISS / Bacon–Childs–van Dam / Ivanyos–Santha mechanism:
   twisted or entangled coset-state measurements that reduce to a quadratic system over F_p. That
   mechanism is prior, but only for finite groups. The R/Z (infinite-group) version, QZS, was not
   found anywhere as a stated problem, and no algorithm for it was found.
4. **QZS itself.** The existence theory for small fractional parts of quadratic forms is classical:
   * Heilbronn 1948;
   * Danicic;
   * Cook 1980;
   * Baker 1981;
   * Schinzel–Schlickewei–Schmidt (SSS) 1980.

   SSS's title, "Small solutions of quadratic congruences and small fractional parts of quadratic
   forms", indicates the same architecture as SDA-ISO: pass from fractional parts to a congruence
   modulo a denominator q. **I could not open SSS (HTTP 403).** Under TRAPS 10, whether SSS's
   proof is the SDA-ISO argument stays **UNKNOWN**, but it is the most likely method-level prior
   art and must be read by a human. The individual algorithmic steps are standard:
   * LLL simultaneous Diophantine approximation (LLL 1982; Lagarias 1982/85);
   * a modular square root (Tonelli–Shanks);
   * Gauss reduction of the 2-D lattice {μ₁ ≡ rμ₂ mod q} (Hermite–Serret/Cornacchia-type).

   No source was found that states QZS as an algorithmic problem or proves it easy or hard.
   Lagarias' NP-hardness of SDA needs growing dimension and sup-norm-best approximations. It does
   not apply to the fixed-dimension (n = 2), slack-tolerant regime SDA-ISO uses, and Lenstra-type
   fixed-dimension algorithms are polynomial there. Status: **no algorithmic prior art found for
   QZS. The method is plausibly classical (SSS, unread).**

## Relevant papers, with locators and relation to Theorems A and C′

[read] = the text, or the named sections, were read. [abs] = abstract only. [snip] = search
snippet or secondary statement only. [403] = the fetch was refused.

### Infinite groups

| # | Paper | Locator | What it proves | Relation |
|---|---|---|---|---|
| 1 | G. Kuperberg, *The hidden subgroup problem for infinite groups* | arXiv:2507.18499v1 (24 Jul 2025, only version; 44 pp.) [read: local pdftotext `2026-11-12-rees-h3z-referee/k.txt`, §§1, 4.5, 7] | NP-hardness of HSEP in Q/Z and of NHSEP in non-abelian F_k (Thms 1.1, 1.2). SVP reduces to HSP in Z^k with pseudo-polynomial query cost (Thm 1.4). Polynomial-time HSP in Z^k for any rank (Thm 1.5/7.1). Stretched-exponential time for virtually abelian groups (Cor 1.9). §4.5 discusses variations for free groups only. The words "nilpotent", "Heisenberg" and "solvable" do not occur in the text (grep). | **Prior; Theorem A imports Thm 1.5.** It does not treat H_3(Z). Cor 1.9 does not cover H_3(Z) (not virtually abelian). It is unrelated to C′ except that the LLL post-processing is the same kind of tool. |
| 2 | G. Kuperberg, talk slides "The hidden subgroup problem for infinite groups" | math.ucdavis.edu/~greg/adm/oct-29-2020.kuperberg.pdf, slide 25/25 [read] | "Last comments and open problems": HSP is "probably hard for most infinite groups". There "might be a good quantum algorithm for HSP in nilpotent groups". | **Records the problem as open** (2020). |
| 3 | Kuperberg, QIP 2021 slides and abstract | indico.physik.uni-muenchen.de event 84, attachments 455/456 [read] | Prior results listed: Heisenberg over Z/p (BCvD) and 2-step nilpotent (ISS), finite only. | Finite only; open status consistent. |
| 4 | Kuperberg talks, Fields (19 Apr 2022) and Simons (13 Jun 2022) | gfs.fields.utoronto.ca talk page; simons.berkeley.edu/talks/hidden-subgroup-problem-infinite-groups [abs] | HSP in Z^d for any rank via LLL on Fourier samples; Q NP-hard. | Same content as #1; no nilpotent group. |
| 5 | F. Di Concilio, R. Flores, D. Kahrobaei, M. Noce, *From Quantum Mechanics to the Hidden Subgroup Problem: an Overview from Finite to Infinite Groups* | IACR ePrint 2026/2678 (received 2026-10-29) [read: whole pdftotext, scratchpad `eprint2678/2026-2678.txt`; §§8.5, 9, 10 and the reference list rechecked here] | Survey. §8.5 on nilpotent groups cites ISS and RRS (finite) only. §9 on infinite groups covers Kuperberg Thms 1.1, 1.2, 1.5 and Cor 1.9 only. §10 item 5 lists HSP in infinite non-abelian groups, naming lattices in Lie groups, Baumslag–Solitar groups and arithmetic groups, with H_3(Z) "open". The references include Horan–Kahrobaei, Imran–Ivanyos 2022, IMS, ISS and Kuperberg ×3, but not II 2023. | **Records the problem as open** (Oct 2026). No conflict with A or C′. See also `2026-11-12-rees-eprint-2026-2678-check.md`. |
| 6 | K. Horan, D. Kahrobaei, *The Hidden Subgroup Problem and Post-quantum Group-based Cryptography* | arXiv:1805.04179v2 (venue recalled: ICMS 2018) [read: pdftotext, grep] | §5 "Finite, non-abelian" says "(discrete) Heisenberg group", but it describes order-p cyclic subgroups H_{a,b}, which is the finite Heisenberg group over Z_p (BCvD). The infinite subsection says the non-abelian infinite HSP "has not been addressed within the literature". | Unrelated (finite). The word "discrete" there is a misnomer, **not** a claim about H_3(Z). |
| 7 | J. Gryak, D. Kahrobaei, *The status of polycyclic group-based cryptography: a survey and open problems* | arXiv:1607.05819v2 [read: grep] | §2: "there are no known quantum algorithms that are applicable to infinite groups" (2016). | Records the problem as open; out of date (predates Kuperberg). |
| 8 | D. Kahrobaei, R. Flores, M. Noce, *Group-based cryptography in the quantum era* | arXiv:2202.05917v4 (venue recalled: Notices AMS 2023) [read: grep] | §4 open problems include HSP "for various classes of groups … mainly finite". | Records the problem as open; nothing specific. |
| 9 | C. Lomont, *The hidden subgroup problem: review and open problems* | arXiv:quant-ph/0411037 [read: grep] | Infinite groups: abelian only (Lomonaco–Kauffman over R). | Unrelated. |

### Finite nilpotent and Heisenberg groups (the template's finite analogues)

| # | Paper | Locator | What it proves | Relation |
|---|---|---|---|---|
| 10 | G. Ivanyos, L. Sanselme, M. Santha, *An efficient quantum algorithm for the HSP in nil-2 groups* | arXiv:0707.1260v1; LATIN 2008; Algorithmica 62 (2012) [read earlier: `-h3z-imports/sources/iss.txt`] | Finite class ≤ 2 groups, polynomial time. Reduction to exponent-p groups with trivial or cyclic H. Twists solved by Chevalley–Warning over F_p. | **Prior; imported by Theorem A** (through cor:utz). It is the finite analogue of the C′ template. Finite groups only. |
| 11 | Ivanyos, Sanselme, Santha, *An efficient quantum algorithm for the HSP in extraspecial groups* | arXiv:quant-ph/0701235 (venue recalled: STACS 2007) [abs] | Finite extraspecial p-groups. | Finite analogue; unrelated to infinite index. |
| 12 | M. Imran, G. Ivanyos, *Zero sum subsequences and hidden subgroups* | arXiv:2304.08376v1; Quantum Inf. Process. 23 (2024) [read earlier: `-h3z-imports/sources/ii.txt`] | Exact polynomial-time HSP for finite nilpotent groups of constant class with bounded prime factors, via zero-sum subsequences over F_p. Open: a poly(n, p) zero-sum algorithm. The only use of "infinite" is the abelian aside on line 46. | **Prior; imported by Theorem A** (q = 2 case). Its linear zero-sum problem over F_p is distinct from QZS (quadratic, over R/Z). |
| 13 | M. Imran, G. Ivanyos, *An exact quantum hidden subgroup algorithm and applications to solvable groups* | arXiv:2202.04047 (Quantum Inf. Comput. 2022) [abs] | Exact HSP in Z_{m^k}^n; finite solvable groups. | Finite; unrelated. |
| 14 | G. Ivanyos, M. Santha, *On solving systems of diagonal polynomial equations over finite fields* | arXiv:1503.09016v2 (venue recalled: FAW 2015 / TCS) [abs] | Solves diagonal polynomial systems over F_p and applies this to HSP in some semidirect-product p-groups of constant class. Open: nonzero solutions of systems of more than one equation. | **Closest finite analogue of QZS** (diagonal quadratic forms with a zero-sum condition, over F_p). Different domain: QZS is over R/Z, with a size bound. |
| 15 | D. Bacon, A. Childs, W. van Dam, *From optimal measurement to efficient quantum algorithms for the HSP over semidirect product groups* | arXiv:quant-ph/0504083 (venue recalled: FOCS 2005) [abs] | PGM on several coset states for Z_p^r ⋊ Z_p, including the Heisenberg group over Z_p. It reduces to quadratic equations mod p. | Finite analogue of the C′ measurement-and-equation step. |
| 16 | J. Radhakrishnan, M. Rötteler, P. Sen, *On the power of random bases in Fourier sampling: HSP in the Heisenberg group* | arXiv:quant-ph/0503114 (ICALP 2005, per ePrint 2678 refs) [abs] | Finite Heisenberg group: random-basis strong Fourier sampling. | Finite; a different mechanism. |
| 17 | D. Bacon, *How a Clebsch–Gordan transform helps to solve the Heisenberg HSP* | arXiv:quant-ph/0612107 [abs] | Finite Heisenberg group, representation-theoretic. | Finite; unrelated to infinite index. |
| 18 | H. Krovi, M. Rötteler, *An efficient quantum algorithm for the HSP over Weyl–Heisenberg groups* | arXiv:0810.3695 [abs] | Finite Weyl–Heisenberg groups, 2 coset states per round. | Finite; unrelated. |
| 19 | K. Friedl, G. Ivanyos, F. Magniez, M. Santha, P. Sen, *Hidden translation and translating coset* | arXiv:quant-ph/0211091 (venue recalled: STOC 2003) [abs] | Finite solvable groups of constant exponent and derived length. | Finite; unrelated. |

### Recent (2025–2026) HSP papers screened, all unrelated

| # | Paper | Locator | Finding |
|---|---|---|---|
| 20 | S. Dutto, P. Mercuri, N. Murru, L. Romano, HSP survey (cites Kuperberg) | arXiv:2512.02087 [abs] | Abelian, dihedral, symmetric and semidirect cases; no H_3(Z). |
| 21 | A. Te'eni, Y. Oz, E. Cohen, *One-query algorithms for the index-q HSP* (cites Kuperberg) | arXiv:2510.10538v2 [abs] | Abelian index-q; unrelated. |
| 22 | I. Holt, S. Subramanian, *Learning quantum symmetries* (cites Kuperberg) | arXiv:2609.38085v2 [abs] | StateHSP with normal H, finite groups; unrelated. |
| 23 | Kuperberg citations, other | Semantic Scholar list: arXiv:2508.08823 (hard DLP instances), 2508.04819 (oscillator–qudit), J. Cryptology 10.1007/s00145-025-09546-5 [titles only] | Unrelated by title. Not opened. |
| 24 | M. E. S. Morales, *HSP in semidirect products and quasi-Hamiltonian groups* | arXiv:2608.05321v2 [abs] | Finite groups only. |
| 25 | A. Miasnikov, A. Ushakov, *Quantum polynomial-time conjugacy in metabelian groups* | arXiv:2610.27250v1 [abs] | Conjugacy problem, not HSP; metabelian finitely presented groups. H_3(Z) is metabelian, but this is a different problem. Unrelated. |
| 26 | O. O'Brien, trapped-ion non-abelian HSP | arXiv:2611.06716v1 [abs] | Finite Z_q ⋉ Z_p experiment. |
| 27 | Dong, Fan, Zhong, Qiu, generation bounds for finite nilpotent groups | arXiv:2511.19494; AIMS Math. 11(4) 2026 [read: first page] | Finite abelian HSP repetition counts. |
| 28 | Gheorghiu, Jacobs, Mehraban, Motamedi, *Quantum state isomorphism problems for groups* | arXiv:2605.12615v2 [abs] | State hidden-shift analogue; unrelated. |

### Quadratic zero-sum (QZS): Diophantine and algorithmic background

| # | Source | Locator | Content | Relation to QZS / SDA-ISO |
|---|---|---|---|---|
| 29 | A. Schinzel, H. P. Schlickewei, W. M. Schmidt, *Small solutions of quadratic congruences and small fractional parts of quadratic forms* | Acta Arith. 37 (1980) 241–248, doi:10.4064/aa-37-1-241-248 [403; statement via #30] | Every quadratic form in n variables has a nonzero solution mod q of size ≪ q^{1/2+1/(2n)} for n odd and ≪ q^{1/2+1/(2n−2)} for n even (Heath-Brown's restatement). By its title it also deduces small-fractional-part results. | **Likely method-level prior art** for passing from a congruence mod q to fractional parts. **UNKNOWN until read.** Existence only, as far as seen; no algorithm seen. |
| 30 | D. R. Heath-Brown, *Small solutions of quadratic congruences, and character sums with binary quadratic forms* | arXiv:1411.4816 [read: §1] | Survey of B_n(q). B_n(q) ≥ q for n = 1, 2 and square-free q in the worst case. Cites Baker, *Diophantine Inequalities*, Ch. 9. Uses a 2-D lattice of determinant ‖a₀‖ and its shortest vector. | Context. The worst-case lower bound for n = 2 shows why SDA-ISO needs q prime with −c₂/c₁ a QR (its Lemma Q). The 2-D shortest-vector step is the same tool. |
| 31 | R. J. Cook, *Small fractional parts of quadratic forms in many variables*, Mathematika (1980); R. C. Baker, *Small fractional parts of quadratic and additive forms*, Math. Proc. Camb. Phil. Soc. (1981); Danicic (1958) | Cambridge Core landing pages [snip; paywalled] | Existence: nonzero x with ‖Q(x)‖ ≤ N^{−c(n)+ε} for |x| ≤ N. | Existence theory for exactly the QZS inequality, with no algorithm. In QZS's regime (|μ| ≤ 2^{poly K}), existence is trivial even for n = 1 (Heilbronn). Only efficiency is at issue. |
| 32 | Heilbronn 1948; Zaharescu (exponent 4/7); "Simultaneous small fractional parts of polynomials", GAFA 2021 (author recalled as Maynard, not verified) | [snip] | ‖n²α‖ ≪ N^{−1/2+ε} for some n ≤ N; simultaneous versions. | Existence; n = 1 and simultaneous analogues. No polynomial-time construction found for n = 1. QZS with n = 2 sidesteps this. |
| 33 | J. C. Lagarias, *The computational complexity of simultaneous Diophantine approximation problems*, SIAM J. Comput. 14 (1985); FOCS 1982 | [snip] | Good SDA (sup norm, denominator range) is NP-complete in growing dimension. LLL gives approximations within a 2^{O(d)} factor in polynomial time. Lenstra-type fixed-dimension best approximations are polynomial. | SDA-ISO uses dimension 3 with slack, so the hardness does not apply. It relies on LLL 1982, which is standard. |
| 34 | J. M. Pollard, C. P. Schnorr, *An efficient solution of the congruence x² + ky² ≡ m (mod n)*, IEEE Trans. IT 33 (1987) | [snip] | Finds any solution (not a small one) without factoring n. | Background only. SDA-ISO uses a prime q and Tonelli–Shanks instead. |

## Searches run (all on 2026-11-12)

WebSearch, with the mode in brackets:
1. `hidden subgroup problem discrete Heisenberg group integers quantum algorithm` [extended]
2. `Kuperberg "hidden subgroup" infinite groups 2507.18499`
3. `"hidden subgroup problem" "nilpotent" "infinite index" quantum`
4. `hidden subgroup problem infinite groups Baumslag-Solitar quantum algorithm`
5. `Horan Kahrobaei hidden subgroup problem infinite groups`
6. `"hidden subgroup" "Heisenberg group" infinite OR "over the integers" arXiv 2026` [extended]
7. `"hidden shift" Heisenberg group quantum algorithm`
8. `quantum algorithm hidden subgroup finitely generated nilpotent group polycyclic group infinite`
9. `"hidden subgroup problem" Heisenberg group H_3(Z) open problem infinite non-abelian efficient` [extended]
10. `algorithm find integer n with small fractional part of n^2 alpha Heilbronn constructive` [extended]
11. `computational complexity simultaneous Diophantine approximation NP-hard Lagarias quadratic forms fractional parts algorithm`
12. `small fractional parts of quadratic forms diagonal Schmidt Baker Cook Diophantine inequalities n variables bound`
13. `Schinzel Schlickewei Schmidt "small solutions of quadratic congruences and small fractional parts of quadratic forms"`
14. `efficient algorithm small solutions quadratic congruence x^2 + k y^2 = 0 mod n lattice Pollard Schnorr`
15. `polynomial time algorithm "small fractional parts" quadratic form lattice reduction random coefficients`
16. `quantum algorithm hidden subgroup "Heisenberg group" lattice "Diophantine approximation" coset state infinite`
17. `"hidden subgroup" unitriangular matrices over integers quantum UT_n(Z)`
18. `"discrete Heisenberg group" quantum algorithm hidden subgroup OR "period finding" OR "hidden shift"` [extended]
19. `Ivanyos Sanselme Santha nil-2 hidden subgroup follow-up nilpotent class 3 quantum polynomial time 2024 2025 2026`
20. `"fractional parts" "quadratic" Diophantine approximation algorithm "NP-hard" OR "polynomial time" integer x with ||alpha x^2|| small`
21. `Danicic Cook "small fractional parts" additive quadratic form n variables N^{-n/2} exponent`
22. `quantum hidden subgroup problem nilpotent Lie group OR "lattice in a nilpotent Lie group" OR "real Heisenberg group" algorithm`
23. `"2507.18499" hidden subgroup` [extended]
24. `Kuperberg "hidden subgroup problem for infinite groups" nilpotent OR Heisenberg OR "virtually nilpotent" follow-up 2026`
25. `"Zero sum subsequences and hidden subgroups" cited`

arXiv API (`export.arxiv.org/api/query`), sorted by submission date, newest first:
* `all:"hidden subgroup" AND all:Heisenberg`: 5 hits, all finite.
* `all:"hidden subgroup" AND all:nilpotent`: 7 hits, all finite.
* `all:"hidden subgroup" AND all:infinite`: 5 hits.
* `abs:"hidden subgroup" AND (polycyclic OR "finitely generated" OR "Lie group" OR unitriangular OR "discrete group")`: 3 hits.
* `abs:"hidden subgroup" AND (Diophantine OR "lattice reduction" OR LLL)`: 1 hit.
* `abs:"hidden subgroup" OR abs:"hidden shift"`: 205 total. The 47 newest were screened, covering 2024-01 to 2026-11-04.
* `abs:"hidden subgroup" AND ("nilpotency class" OR "zero sum" OR "nil-2" OR "p-groups")`: 5 hits, all finite.
* `abs:quantum AND abs:algorithm AND (nilpotent OR Heisenberg OR polycyclic) AND cat:(math.GR|cs.CC|cs.DS)`: 28 hits.
* Author listings: `au:Ivanyos` (2020–2026), `au:Santha AND abs:subgroup`, `au:Kuperberg AND ti:hidden`.
* Abstract pages: 2507.18499, 2609.38085, 2512.02087, 2510.10538, 2608.05321, and id_list 2610.27250, 2611.06716, 2609.10596, 2605.12615, 2610.16827.

Other services:
* Semantic Scholar: citations of arXiv:2507.18499 returned 7 entries. Later queries returned HTTP 429.
* dblp: the API was blocked (Anubis).
* Direct downloads (arxiv.org, the author's own page, LMU indico): 1805.04179, 1607.05819, 2202.05917, quant-ph/0411037, 1411.4816, and Kuperberg's 2020 and QIP 2021 slides and abstract.

## Limits of the search

* **Not accessed:** Google Scholar ("cited by" for Kuperberg, ISS and II). Semantic Scholar was
  rate-limited after one query. dblp was blocked. **Citations of ISS 2012 and II 2023 were
  therefore searched only through arXiv full-database abstract queries, not citation graphs.**
* **Paywalled or refused (HTTP 403):**
  * SSS 1980, the key unread item; the ICM full-text mirror refused;
  * Cook 1980, Baker 1981, Danicic, Lagarias 1985, Pollard–Schnorr 1987;
  * the GAFA 2021 paper;
  * the ePrint PDF by URL (the copy the owner downloaded was used instead);
  * journal versions of ISS (Algorithmica) and II (QIP).
* **Abstract-level only.** The arXiv API matches abstracts and titles, not full text. A paper
  that solves H_3(Z) inside a section, without saying so in its abstract, would be missed. Most
  of the finite-group papers in the tables were classified from abstracts.
* **Recency.** The newest arXiv entry seen is from 2026-11-04. Anything posted after about
  2026-11-10, or not yet indexed by the web search engine, is not covered. ePrint was checked
  only for 2026/2678.
* **Not covered:** Non-English literature, theses, MathSciNet/zbMATH reviews, and talks beyond
  Kuperberg's.
* No specialist was consulted. Absence of evidence is not evidence of absence (TRAPS 8, 10).

## Claims that must stay false

* `novelty_established` (any repo gate) stays false.
* No claim that the ePrint 2026/2678 open problem is solved. Theorem C′ is PROVED given cited
  theorems in one AI session and is not refereed.
* No claim that QZS, SDA-ISO or its method is new. SSS 1980 is unread and likely overlaps at the
  method level.
* No claim of hardness for any case.

## Next question and acceptance test

* **Human:** read SSS 1980 (Acta Arith. 37, 241–248) and Baker, *Diophantine Inequalities*
  (1986) Ch. 9. Decide whether the SDA → congruence mod q → small-solution argument appears there,
  and in what form. Accept "method prior" if SSS's proof uses a Dirichlet common denominator plus
  a small solution of the induced quadratic congruence. Then cite it in any write-up of Theorem C′.
* **Specialist query** (to an HSP expert, e.g. through the existing correspondence): is HSP in
  H_3(Z) for infinite-index H known or folklore? Ask this after the hostile referee of C′, not
  before.
* **Re-run** Google Scholar "cited by" for arXiv:2507.18499, 0707.1260 and 2304.08376 from a
  browser the owner controls.

## Adversarial self-check

* *Could a paper solve H_3(Z) without saying so in its abstract?* Yes. For example, a remark
  could reduce H_3(Z) to virtually abelian groups after quotienting by H ∩ Z. That remark covers
  only Theorem A's case and gives only 2^{O(√n)} time via Kuperberg Cor 1.9. Theorem A's
  polynomial bound would still differ. The cyclic H ∩ Z = 1 case has no such reduction:
  H_3(Z) itself is not virtually abelian.
* *Is the survey's "open" statement informed?* It misses II 2023 (finding 1 of the earlier
  check), so it is not exhaustive. Kuperberg's own 2020 remark is the stronger signal. Both are
  statements of belief, not literature proofs of absence.
* *Is Horan–Kahrobaei's "(discrete) Heisenberg group" a prior claim?* No. The text describes
  order-p subgroups H_{a,b}, which is the finite group over Z_p of BCvD, and its infinite section
  says the non-abelian infinite case has not been addressed. I read this from the PDF text, not a
  summary.
* *Did I over-weight SSS from its title alone?* I mark its relation UNKNOWN for that reason.
  The overlap could also be smaller, for example existence only, with a different pigeonhole
  argument and no isotropic line. Either way it does not make QZS's algorithmic statement prior
  art. It would make the idea classical.
* *Kuperberg Thm 1.4 (SVP reduces to HSP in Z^k with pseudo-polynomial query cost).* This is a
  hardness-flavoured result in a **different access model** (oracle cost poly(‖x‖₁), unary). It
  does not bear on Theorem A, which uses the binary, standard-query Thm 1.5. Checked in §6 of
  the local k.txt.
* *Model mismatch risk.* The local model uses signed boxes |entries| < 2^B, size parameter b and
  label width w (`-h3z-infinite-index.md` §0). A future paper in a different encoding (words,
  Mal'cev coordinates, compressed words) would be a "different model" item and should not be
  read as either prior or conflicting.
