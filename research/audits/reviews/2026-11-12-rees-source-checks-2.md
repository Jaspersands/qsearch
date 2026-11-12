# Rees papers: second source pass on the NEEDS HUMAN items (2026-11-12)

AI-only check (one Claude agent), pending human review. No paper file and no earlier report was
edited. It follows `2026-11-12-rees-source-checks.md` (the "first report").
Line numbers are those of the working tree at the start of this pass.

Folder `2026-11-12-rees-source-checks-2/`:
- `sources/` holds pdftotext extractions of the open copies read here. They are untrusted data.
- `scripts/` holds two falsification checks; their outputs are `*.out`.

Sources fetched (all legitimate open copies):
- arXiv: quant-ph/9903071v1, 2202.04047v3, quant-ph/9508027v2, and the abs pages of
  quant-ph/0401083 and 2202.04047.
- The published QIC version of Imran–Ivanyos 2022, from the SZTAKI institutional repository
  (eprints.sztaki.hu/10362).
- AKS, Annals 160 (2004), the PDF on annals.math.princeton.edu, and the AKS preprint v6 (IIT Kanpur).
- Lenstra–Pomerance, "Primality testing with Gaussian periods", version 20090807 (author page,
  math.dartmouth.edu).
- Luks's author copy (ix.cs.uoregon.edu).
- Landing pages for IACR ePrint 2013/069, Springer (MP13 and Mosca–Ekert) and the Annals.

Blocked or paywalled:
- IEEE Xplore (Luks FOCS): empty response.
- ScienceDirect (EHK, IPL): HTTP 403.
- IACR archive and ePrint PDFs (MP13): HTTP 403.
- Springer full texts: paywalled.
- DBLP: bot wall.
- Numdam (Lazard 1954): the scan is over the 10 MB fetch limit.

Verdicts: CONFIRMED, WRONG (replacement text given), STILL NEEDS HUMAN (reason given).

## Summary

| Item | Verdict |
|---|---|
| A1 Luks Thm 3.2(5) | Author copy CONFIRMED. FOCS numbering STILL NEEDS HUMAN. Priority of Theorem W STILL NEEDS HUMAN, but nothing printed claims it. |
| A4 Khukhro 1998 | STILL NEEDS HUMAN. The book is not legally available beyond the Google Books preview. Nothing printed depends on item (i). |
| A6/A22 EHK | arXiv content CONFIRMED again. IPL numbering STILL NEEDS HUMAN (ScienceDirect blocked). |
| A9/A21 AKS | **CONFIRMED in the Annals version**: Thm 5.1, p. 789; Lemma 5.2, p. 790; Thm 5.3, p. 791. The 15/2 is real, and its constant rests on Fouvry's unspecified constants. Adopting it stays an owner decision. New option: the Lenstra–Pomerance exponent 6, which is effective. |
| A15 MP13 | Author version CONFIRMED. CRYPTO numbering STILL NEEDS HUMAN (paywalled or 403). A search snippet suggests "Theorem 1 (Corollary of Theorem 4)". Wording fix proposed. |
| A17 Jacobi / Kronecker / Module-SIS | Printed claims CONFIRMED (mathematics, plus a finite falsification check). The negative literature claim sits only in a tex comment, and the printed text says no such result is used or claimed. Nothing is left for a human, apart from rewording the comment. |
| II22 theorem number | **CONFIRMED in both arXiv v3 and the published QIC version**: Theorem 2 and §4.2. |
| Mosca–Ekert §§2, 4.2 | Locators CONFIRMED for arXiv v1; LNCS numbering not checked (paywalled). ME prove no formal period-finding theorem. With Q ≥ 2R², a good outcome recovers k/e in lowest terms exactly, not e itself. **The core's repetition count O(log(m/ε)) is not justified** for its single-candidate acceptance test. It needs an extra factor log(b+1), or the lcm trick. The bound stays polynomial. Replacement text below. |

## Items

### A1. Luks Theorem 3.2(5), and the priority of Theorem W

- **Paper.**
  - appendix-filters.tex:29: "By Luks [Theorem 3.2(5)] the stabilizer is computable classically
    for every matrix p-group acting by conjugation".
  - :35: rem:filters(0) cites "[Theorem 3.2(5),(7)]".
  - :49 ends with "the combination may be known" and the tag "priority of Theorem W ... Luks
    Theorem 3.2(5) numbering not checked offline".
- **Source.** Luks, "Computing in Solvable Matrix Groups", author copy
  (`sources/luks_solmatgrp_author_copy.txt`:181–212).
  - Thm 3.2 runs in time polynomial in n + log|F| + ν, where ν is the largest prime dividing |G|
    other than the characteristic.
  - Item (5) is "Given any vector v ∈ F^n, find the subgroup of G that fixes v".
  - Item (7) is the subspace stabilizer.
  - The author copy has its own page numbers (its p. 4 carries Thm 3.2), not the FOCS pages
    111–120, so it is not the printed version. IEEE Xplore (doc. 267813) returned nothing.
- **Use.** For a p-group in characteristic p, ν adds nothing. Conjugation on a k-tuple of N×N
  matrices is a linear action of dimension kN², so (5) applies to the image group, which is a
  p-group and hence solvable.
- **Verdict.**
  - Locator: CONFIRMED in the author copy. FOCS numbering STILL NEEDS HUMAN, because IEEE Xplore
    is not reachable.
  - Priority of Theorem W: STILL NEEDS HUMAN. It is a novelty question about the coding-theory
    and polynomial-symmetry literature (Kayal 2011), and no single primary source can settle a
    negative.
  - The printed text names no "Theorem W" and claims no priority. It says the ingredients "are
    classical, and the combination may be known". Nothing printed is at risk.
  - Suggested tag text: "Luks Thm 3.2(5),(7) checked in the author copy (ix.cs.uoregon.edu/~luks/solmatgrp.pdf); FOCS printing not compared".

### A4. Khukhro 1998, the residual locators

- **Paper.** main.tex:457 (proof), and the tag at :458–461:
  - (i) the statement and page of Lemma 9.15, which is not cited;
  - (ii) a book locator for γ_k(G) = γ_k(L) for all k, which the text attributes to Lazard1954
    with no locator.
- **Source.** The CUP book is paywalled on Cambridge Core. The publisher-authorised Google Books
  preview used on 11-09 lacks pp. 108, 110, 112, 116 and 122–123, where Lemma 9.15 and Theorems
  10.19–10.23 lie (see `2026-11-09-khukhro-locators.md`).
  - Lazard, Ann. Sci. ÉNS 71 (1954) 101–190 (doi 10.24033/asens.1021), is openly on Numdam
    (numdam.org/item/ASENS_1954_3_71_2_101_0). Its PDF exceeds the fetch limit, so it was not read.
- **Verdict.** STILL NEEDS HUMAN, because no legal full text of the book was available.
  - (i) No printed text depends on it.
  - (ii) A human can locate the statement in Lazard 1954 on Numdam.
  - Fallback (argued here, AI only, not checked): the reverse inclusion
    γ_k(L) ⊆ γ_k(G) follows by induction on k from the inverse formulas
    [x,y] = (x,y)·∏κ_j^{s_j} and x+y = xy·∏κ_j^{r_j}, with group commutators κ_j of weight
    ≥ 3 and ≥ 2 respectively. These are Khukhro Lemma 10.7 (p. 115, confirmed 11-09),
    transferred to the Lazard setting on p. 124. Each κ_j involves an entry from γ_{k−1}(G) and
    one other entry, so it lies in γ_k(G).

### A6/A22. Ettinger–Høyer–Knill, IPL numbering

- **Paper.**
  - main.tex:1222 and core/main-core.tex:895 cite Theorem 2 for O(log²|G| + log(1/ε)) queries
    and Theorem 1 for O(log⁴|G|) queries with exponentially small error.
  - The tags are at main.tex:1223 and core:896.
- **Source.** arXiv quant-ph/0401083 has a single version, v1 of 14 Jan 2004. Its journal-ref
  is IPL 91(1) 43–48 (16 July 2004), doi 10.1016/j.ipl.2004.01.024.
  - Thm 1 (local text `2026-11-02-rees-classical-lower-bound/refs/quant-ph_0401083.txt`:70):
    O(log⁴|G|) calls, "fails with probability exponentially small"; it can also be made exact
    with arbitrary one-qubit gates.
  - Thm 2 (:124): Prob[H|H] ≥ 1 − 4r/2^{s/2}, with s ∈ Θ(n² + log(1/ε)).
  - ScienceDirect returned HTTP 403, and no author copy of the IPL typesetting was found.
- **Verdict.** CONFIRMED for arXiv v1. IPL numbering STILL NEEDS HUMAN.
  - Optional wording: "(numbering of arXiv:quant-ph/0401083, the version accepted by IPL)".
  - The arXiv comment reads "To appear in Information Processing Letters". That makes a
    renumbering unlikely, but it is not checked.

### A9/A21. AKS: the Õ(log^{15/2} n) bound

- **Paper.**
  - Printed: appendix-torsion-blackbox.tex:1612 uses "Õ(ℓ^{21/2}) bit operations each [AKS2004]",
    and main.tex:1426 uses "Õ(sℓ^{23/2}) for the primality certificates".
  - The tags at main.tex:1430–1439 and appendix-torsion-blackbox.tex:1561–1571 ask whether
    AKS Theorem 5.3 gives 15/2.
- **Source.** The Annals 160 (2004) 781–793, from the journal's PDF
  (`sources/aks_annals_2004.txt`; page headers at lines 384, 435 and 496):
  - Thm 5.1, p. 789: "O∼(log^{21/2} n)".
  - Lemma 5.2 [Fou], p. 790: "There exist constants c > 0 and n0", with c and n0 not given.
  - Thm 5.3, p. 791: Õ(log^{15/2} n), proved from Lemma 5.2.
  - The introduction (p. 782) states 15/2 as the main result, and 21/2 as the bound that needs no
    sieve theory.
  - Preprint v6 numbers these the same way (`sources/aks_preprint_v6.txt`:355, 408, 414).
  - On ineffectivity, Lenstra–Pomerance (version 20090807, `sources/lenstra_pomerance_aks080709.txt`:61–62)
    write that AKS "also prove a result with run time exponent 15/2 in which c is not effectively
    computable". This is a secondary source. AKS themselves only leave the constants unspecified.
- **Verdict.** CONFIRMED, Annals numbering included.
  - The printed 21/2 is Theorem 5.1, p. 789.
  - The tags can drop "Annals numbering not checked" and "not confirmed offline".
  - Whether to adopt 17/2 is an owner decision. The implied constant of 17/2 rests on
    Fouvry's constants, which AKS do not give and LP call not effectively computable.
- **New alternative (not adopted, owner decision).** LP Theorem 1 (`sources/...aks080709.txt`:52–54)
  gives a deterministic test in time (log n)^6·(2 + log log n)^{c0} with c0 effectively
  computable.
  - It is a modified algorithm. The certificate cost would become Õ(ℓ^7), effective.
  - The consequences listed in the tags would need redoing, because the O(ℓ^8) normalizer term
    and the O(ℓ^9) fallback would then dominate at c = 1.
  - The published-version (JEMS) numbering was not checked.

### A15. Micciancio–Peikert 2013, Theorem 1.1

- **Paper.** appendix-free-coordinate.tex:283 has "by [Theorem 1.1]{MicciancioPeikert2013} …
  within Õ(√(M_d g_d))". The tag is at :287. The bib entry is CRYPTO 2013, LNCS 8042, pp. 21–39.
- **Source.** The author version of 13 Feb 2013 (local `2026-11-02-rees-linear-arity/lit/mp13_LWsE.txt`:105)
  has "Theorem 1.1 (Corollary of Theorem 3.8)".
  - It gives SIS with solution set {‖z‖₂ ≤ β, ‖z‖∞ ≤ β∞}∖{0} and q ≥ β·n^δ, and approximation
    γ = max{1, ββ∞/q}·Õ(β√n).
  - With β = √M, β∞ = 1, n = g_d and q = p ≥ √M·g_d^θ, this gives Õ(√(M g_d)). That matches.
  - ePrint 2013/069 is "A minor revision of an IACR publication in CRYPTO 2013", with its last
    revision on 2019-10-04. Its PDF and the IACR archive PDF returned 403.
  - The Springer chapter is paywalled; its landing page confirms pp. 21–39.
  - A search-engine snippet of the Springer PDF reads "Theorem 1 (Corollary of Theorem 4)". It
    was not read, so it is not evidence.
- **Verdict.** CONFIRMED for the author version. CRYPTO numbering STILL NEEDS HUMAN. The
  numbering probably differs.
  - Replace "\cite[Theorem~1.1]{MicciancioPeikert2013}" by
    "\cite[Theorem~1.1]{MicciancioPeikert2013} (numbering of the authors' version of 13~February~2013; IACR ePrint 2013/069)".
  - Alternatively, a human with Springer access can substitute the CRYPTO number.

### A17. Jacobi sums, Kronecker, and Module-SIS modulo a degree-one prime

- **Paper.**
  - appendix-free-coordinate.tex:315 has the Jacobi-sum count: at least
    (p − (κ−1)(κ−2)√p − 3κ + 1)/κ² pairs; and the probability ≥ 1/(2κ) once
    √p ≥ 2(κ−1)(κ−2)+4.
  - :321 has "by Kronecker's theorem, exactly the vectors of canonical ℓ∞-norm at most 1", for
    even h, and the sentence "No worst-case hardness result for this modulus is used or claimed."
  - The tag at :322 lists all three facts "from memory", including "the absence of a worst-case
    reduction for Module-SIS modulo a degree-one prime ideal".
- **Source and check.**
  - Jacobi: |J| = √p was confirmed in the first report (A13: math, plus 2624 exact cases). A new
    falsification check, `scripts/jacobi_count_check.py`, brute-forced the count bound and the
    1/(2κ) bound for every prime p ≤ 2000 and every κ | p−1 with κ ≥ 2, at one y per coset:
    0 failures in 600753 cases (`jacobi_p2000.out`). This can only falsify; it proves nothing.
  - Kronecker: an algebraic integer whose conjugates all have modulus ≤ 1 is 0 or a root of unity.
    The roots of unity in Q(ζ_h) are μ_h for even h. So canonical ℓ∞ ≤ 1 in Z[ζ_h] means
    coordinates in μ_h ∪ {0}. This is CONFIRMED (standard mathematics). No bib entry is printed,
    so no locator is owed.
  - Module-SIS: the printed text asserts nothing about the literature. The negative claim exists
    only in the tex comment.
- **Verdict.** The printed claims are CONFIRMED, with nothing left for a human.
  - Replace the tag by: "% Jacobi-sum count checked by brute force for p <= 2000 (source checks 2026-11-12-2); Kronecker standard; no Module-SIS hardness claimed, so no literature check needed."
  - If the authors later want to say that no reduction exists, a lattice specialist must check
    that. It is not currently said.

### Imran–Ivanyos 2022 theorem number (first report, disposition line 88)

- **Paper.**
  - main.tex:1403, core cor:nilpotent and appendix-torsion-blackbox.tex cite
    "\cite[Theorem~2 and Section~4.2]{ImranIvanyos2022}".
  - The tags are at main.tex:1404 and appendix-torsion-blackbox.tex:708.
  - The bib entry is QIC 22(9&10):770–789.
- **Source.**
  - arXiv 2202.04047v3 (2 May 2022; v1 and v2 date from Feb 2022), `sources/imran_ivanyos_2022_arXiv_2202.04047.txt`:
    Thm 2 is at :275; task (i) is "Compute the uniform superposition of elements of G"; §4.2,
    "Computing the uniform superposition of group elements", is at :832.
  - The published version is headed "Quantum Information and Computation, Vol. 22, No. 9&10
    (2022) 770–789 c Rinton Press" (SZTAKI repository PDF, `sources/imran_ivanyos_2022_QIC_sztaki.txt`).
    There Thm 2 is at :276 with the same text, and §4.2 has the same title, at :818.
  - Theorem 2 uses the group oracles, QFT_m and their inverses, for solvable G with |G| | m^k.
  - §4.2 states no reset of the workspace, which is consistent with the B2c wording already applied.
- **Verdict.** CONFIRMED in both the arXiv v3 and the published QIC version. Both tags can be
  deleted.

### Mosca–Ekert, quant-ph/9903071, Sections 2 and 4.2

- **Paper.**
  - core/main-core.tex:814 (and main.tex:1458) cites §2 for "HSP for finitely generated groups
    and hidden subgroups of finite index" and for the reduction of the abelian case to a finite
    group.
  - core:826 (and main.tex:1470) has "Period finding for such functions [Section 4.2] …, run on
    0 ≤ t < 2^{2b+1}, returns candidates r". A candidate r ≤ 2^b is accepted if f(I+rE_ij) = f(I).
    The text then says "Repeating O(log(m/ε)) times per pair makes the probability that some pair
    has no accepted candidate at most ε/4".
- **Source** (arXiv v1, the only version; its comment says it is the version for the QCQC
  proceedings). `sources/mosca_ekert_quant-ph_9903071.txt`:
  - §2 (:61–112): f from a finitely generated G, constant and distinct on the cosets of K, of
    finite index. For each generator e_j, "use the algorithm in Sect. 4.2 to find an integer k
    such that f(ke_j) = f(0)", and then assume G is finite. Running times are *expected* times.
  - §4.1 (:220–290): estimate a random eigenvalue "with accuracy 1/2r²". The denominator of k/r
    in lowest terms "will be a factor of r". Choose l > 2 log₂ r (so Q = 2^l > r²), apply
    continued fractions, and "repeat O(1) times to find r". There is no proof, only a reference
    to Shor.
  - §4.2 (:311–374): the same analysis for any f : Z → X injective on a period, with the
    estimate "with just O(1) applications of the operator U_f".
  - ME state **no theorem**, **no Q ≥ 2R² condition**, and no success probability.
- **Mathematics (PROVED, standard).** Let Q ≥ 2R² and e ≤ R, and call x good if
  |x/Q − k/e| ≤ 1/(2Q) for some k. Then |x/Q − k/e| ≤ 1/(4R²) < 1/(2e²).
  - So the reduced form of k/e is a convergent of x/Q, by Legendre's theorem.
  - It is also the unique fraction with denominator ≤ R within 1/(2Q) of x/Q, since distinct
    such fractions differ by at least 1/R² > 1/Q.
  - So continued fractions recover **k/e in lowest terms exactly, that is e/gcd(k,e), not e**.
    The period itself comes out only when gcd(k,e) = 1.
  - Shor (arXiv quant-ph/9508027v2, §5, `sources/shor_quant-ph_9508027.txt`:960–985) bounds the
    probability of that event by φ(r)/(3r) "for sufficiently large n". That is Ω(1/log log r), and
    he repeats O(log log r) times. A constant expected number of trials needs small multiples
    [Odlyzko] or the lcm of two candidates [Knill 1995].
- **Finite check** (`scripts/period_finding_check.py`; it can only falsify). It computes the exact
  outcome distribution for Q = 2^{2b+1}, R = 2^b, and every period e ≤ R, b ≤ 6, plus
  e ∈ {210, 240, 251, 256} at b = 8, 9.
  - Every good outcome contained k/e (reduced) among its convergents: 0 misses.
  - The per-run probability that the paper's acceptance test passes falls with φ(e)/e: 0.50
    (b ≤ 2), 0.31 (e = 6, 12), 0.25 (e = 30, 60), 0.217 (e = 210, b = 8)
    (`period_b1_b6.out`, `period_b8_b9.out`).
  - There is no constant lower bound; theory says Ω(1/log log e).
- **Verdict.**
  - §2 and §4.2 locators: CONFIRMED for arXiv v1. The LNCS 1509 numbering was not checked
    (Springer paywalled); the landing page confirms pp. 174–188, so the "pages [check]" note in
    references.bib:598 and core/references.bib:468 can go.
  - "Q ≥ 2R² gives exact recovery from good outcomes": TRUE for the reduced fraction, FALSE for
    the period in general.
  - **WRONG (minor, outside citation scope)**: the repetition count at core:826 and main.tex:1470.
    Replace "Repeating $O(\log(m/\eps))$ times per pair" by "Repeating
    $O(\log(b+1)\log(m/\eps))$ times per pair (a run returns $e_{ij}$ itself, and hence an
    accepted candidate, with probability $\Omega(\varphi(e_{ij})/e_{ij}) = \Omega(1/\log(b+1))$,
    \cite[Section~5]{Shor1997})".
  - The corollary's poly_n(b, log(1/ε)) bound is unchanged.
  - Alternative fix: also accept the lcm of any two candidates that are at most 2^b. That restores
    O(log(m/ε)), but needs a source for the constant success probability (Knill 1995, not checked).

## Adversarial self-check

- I matched by content against a numbered statement only where I read the numbered statement in
  the cited version. II22 (QIC) and AKS (Annals) are the only items now confirmed in the version
  the bibliography cites. The Luks, EHK, MP13 and ME numbering stays unverified in the cited
  printed versions.
- The QIC copy came from an institutional repository, not from the publisher site. Its first-page
  header and page range match the bib entry. A post-print with different numbering is possible
  but unlikely, since the header carries the Rinton Press copyright.
- The AKS page numbers come from pdftotext page headers. Thm 5.1 sits between the headers of
  p. 789 and p. 790, so it is on p. 789. The first report's implicit "Thm 5.1 = main bound" is
  unchanged.
- "Not effectively computable" for 15/2 rests on Lenstra–Pomerance, a secondary source. I did not
  read Fouvry 1985.
- The repetition-count finding rests on theory (Shor §5, Hardy–Wright Thm 328 as cited by Shor)
  plus a finite check showing the decline. A finite check cannot prove the asymptotic decay.
  - The paper's "candidates" might be read as including all convergents. My check already
    accepts any convergent denominator ≤ 2^b that is a multiple of e, and still finds 0.217 at
    e = 210.
  - Reading "Period finding [ME §4.2]" as a black box with constant success is not supported by
    ME, who give only expected O(1) and no proof.
- The A17 "nothing left" verdict holds only because the printed text disclaims any Module-SIS
  hardness. If the comment's negative claim is ever printed, it needs a specialist.
- The Khukhro fallback argument is a sketch. It is labelled argued, not checked, and it relies on
  the Lazard-setting transfer on p. 124, which the 11-09 report read.
