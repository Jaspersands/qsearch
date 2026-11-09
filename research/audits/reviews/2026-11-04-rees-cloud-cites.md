# Rees HSP cloud research session: cites

- Session: `session_01B1JoCgtowBkxbmwPsfia8r` (Claude Code cloud session)
- Started: 2026-11-04T01:56Z; final result event: 2026-11-04T02:10Z
- Task: Verify the paper's 40 pinpoint citations (theorem/section/equation numbers) against primary sources.
- Harvested 2026-11-05 from the session's single `result` event via the claude.ai events API.
  Body below is verbatim (SHA-256 of body: `a0a71ffd4059ea4129528cfa4a784208dcc9d29694204b27760dc841a97283bf`, 15681 chars).
- Status: AI-generated, AI-checked only, pending human review. All Rees claim gates stay false.
- Comparison with the paper: `2026-11-04-rees-cloud-research-harvest.md`.

---

I checked all 40 items. **26 are OK, 1 is NOT SUPPORTED (#13), 1 is UNSURE (#21), and 12 are PARTIAL** (#8, 10, 15, 16, 22, 24, 26, 30, 32, 35, 39, 40). No source ended up as NO ACCESS, but #39 and #40 could only be checked through a table of contents and secondary quotations. Nothing was written in the repository, committed, pushed or sent; all downloads are in `/root/cites` only.

I checked items 1–22 and 24–27 myself. Two helper agents checked items 23, 28–40 and 32, and I re-read the key passages for 30, 32, 33 and 38.

## Sources and versions used
| Key | Version used |
|---|---|
| ISS2012 | arXiv 0707.1260v1, the only version. The Algorithmica 62 (2012) text is restricted, so its numbering is unchecked. |
| IvanyosSantha2015 | arXiv 1503.09016v2, the accepted TCS manuscript. |
| ImranIvanyos2023 | arXiv 2304.08376v1, plus the published QIP 23:14 (2024), open access from [eprints.sztaki.hu/10704](https://eprints.sztaki.hu/10704/). Numbering is identical in both. |
| KMOSW2026 | arXiv 2609.40321v1 |
| KOW2026 | arXiv 2510.07515 v1, v2 and v3. Numbering of Thm 2.2, Lemma 3.6 and §5.2 is the same in all three. STOC version not checked. |
| GKSZ2020 | arXiv 1912.04467v2. CCC numbering unchecked. |
| Kitaev1995 | quant-ph/9511026v1 |
| CleveWatrous2000 | quant-ph/0006004v1 |
| IMS2001 | quant-ph/0102014v1. SPAA numbering unchecked. |
| Trappeniers2024 | arXiv 2406.02475 v3, also checked v2 and v1. v1 has a different title ("A Lazard-type correspondence…") and no Theorem 2.3. |
| Kimmel2017 | arXiv 1608.00281v1 and the npj 3:13 PDF plus its Supplementary Information |
| Go2025 | arXiv 2412.02134v3. The IOP PDF could not be fetched. |
| BeneWatts2026 | arXiv 2610.06737v1 |
| ChildsQA | qa.pdf dated 17 April 2025 from cs.umd.edu. The server's root CA (emSign Root CA – G1) was missing from the local trust store; I added only that public root for this one download and did not disable verification. |
| Ye2021 | arXiv 1907.07367v6. ScienceDirect returned 403. |
| Nayak2022 | arXiv 2104.14436v3 |
| EHK2004 | quant-ph/0401083v1 |
| vdW2005 | ISSAC'05 camera-ready PDF from the author's page, and the Leiden thesis (hdl 1887/4392) |
| Luks1992 | the author's own PDF, ix.cs.uoregon.edu/~luks/solmatgrp.pdf, which has its own page numbers |
| Khukhro1998 | CUP front matter (table of contents) and secondary source arXiv 1507.02137v2. The book text was not reachable. |
| LN1997 | secondary sources only: arXiv 2509.08526, 1902.04736, 2403.04312v2 |

## Results
| # | Key | Pinpoint | Verdict | Version | Note / correct number |
|---|---|---|---|---|---|
| 1 | ISS2012 | Thm 2 | OK | 0707.1260v1 | Thm 2: constant class (class closed under subgroups and factor groups) reduces to "p-group of exponent p, subgroup trivial or of cardinality p". The class-2 algorithm itself is Thm 1. |
| 2 | IS2015 | Cor 8 | OK | 1503.09016v2 | Applies only to the family H of order-p subgroups not inside 0×F_p^m, not arbitrary H. Removing the bound on m uses Cor 6 (Thm 3 + Thm 5) together with Prop 7. |
| 3 | IS2015 | Prop 7 | OK | v2 | Polynomial-time quantum reduction of HSP(G,H) to HPGP′(F_p,1,m,d), where d is the class. |
| 4 | IS2015 | Thm 5, §5 | OK | v2 | §5 is a sketch. It assumes p > d and is randomized. It removes the degree-d terms in one step using SDE weights δ_i, then degrees d−1, d−2, … |
| 5 | II2023 | Thm 1 | OK | v1 = QIP | Exact; bounded class and bounded primes; unique encoding; poly(ℓ) operations and poly(log\|G\|) calls to the oracle and its inverse. The oracle returns "an arbitrary (though fixed) purification" of the subgroup state; it is not specifically built from f. |
| 6 | II2023 | §6 / Prop 3 | OK | v1 = QIP | The open problem is a poly(np)-time zero-sum finder for sequences of length (np)^d. Prop 3 assumes a worst-case finder that succeeds with high probability; the average-case remark is in §6 only. |
| 7 | II2023 | §1 | OK | v1 = QIP | "such automorphisms do not exist in general nilpotent groups of class greater than two." |
| 8 | II2023 | Props 1, 2, 4, 5 | PARTIAL | v1 = QIP | See list below. |
| 9 | II2023 | Prop 1 | OK | v1 | Algorithm 1, line 3: K ← N_G(H₀). |
| 10 | II2023 | §2.2 | PARTIAL | v1 | The exact Watrous method is used to prepare \|M₁⟩, a subgroup in the transversal computation. It is not used for G itself. |
| 11 | II2023 | §2.1 | OK | v1 | Assumes exact QFTs modulo the primes of \|G\|; "a constant number of gates are sufficient" for bounded primes. |
| 12 | KMOSW2026 | Thm 1.11 | OK | 2609.40321v1 | m ≥ q^{q²}(n+1)^{q−1}, q a prime ≥ 3, worst case, deterministic, poly(m) time. |
| 13 | KOW2026 | §5.2 | NOT SUPPORTED | v1–v3 | §5.2 only surveys the earlier ISS, IS and II bounds. See list below. |
| 14 | KOW2026 | Thm 2.2 | OK | v1–v3 | Worst-case F₃ⁿ subset sum, deterministic poly(m), for m ≥ (n+1)(n+2)/2; KOW call it a special case of ISS Claim 1. The stronger Thm 1.2 gives n²/3 + Cn log n. |
| 15 | KOW2026 | Lemma 3.6 | PARTIAL | v1–v3 | Lemma 3.6 is only the sparse-dependency step; the count is elsewhere. See list below. |
| 16 | ISS2012 | Claim 1 | PARTIAL | v1 | The bound is right: n′ = (d+1)(d+2)/2 for d equations, p > 2. The algorithm is randomized. See list below. |
| 17 | GKSZ2020 | Def 6.1 | OK | 1912.04467v2 | BIS_q: x ∈ {0,1}ⁿ, x ≠ 0, Ax ≡ 0 (mod q), for n ≥ (m+1)^{N(q)}(q−1). Identifying it with κ = p−1 is your own reading. |
| 18 | IS2015 | Thm 11 | OK | v2 | G(d,m) = d^{d(d−1)/2}(m+1)^d, assuming d \| q−1. The output is a collision (I ≠ ∅, J disjoint, equal d-th-power combinations), not a zero. |
| 19 | IS2015 | Thm 11 + proof of Thm 3, §§3.1–3.3 | OK | v2 | §3.3 states C(d,m) ≤ G(d,m)^{⌈log₂(d+1)⌉}; deterministic (§3.1 avoids nonresidues); works for any input columns, over any F_q. Naming clash: the source's B_ℓ(d,m) = d^{ℓ(ℓ−1)/2}(m+1)^ℓ, so its B_d(d,m) = G(d,m), not your B_d(a). |
| 20 | IS2015 | §3 | OK | v2 | Opening of §3: d′ = gcd(d,q−1) and td = u(q−1)+d′, so x ↦ x^t. |
| 21 | IS2015 | Lemma 12 | UNSURE | v2 | Lemma 12 is a recursion of depth d (ℓ = 1…d). See list below. |
| 22 | IS2015 | Fact 2 | PARTIAL | v2 | Fact 2 needs d+1 variables, not j ≥ 2. See list below. |
| 23 | vdW2005 | §6 | OK | ISSAC'05 + thesis | Thm 6.2: Σ_{i=0}^n x_i^n = 0, n+1 variables, any F_q, deterministic. §6.2: "it is enough to represent −1 in this way". ISSAC Thm 6.2 does not say the solution is nontrivial; thesis Thm 5.3 does (x₀ ≠ 0). |
| 24 | Kitaev1995 | §5, Thm 2, eq. (25) | PARTIAL | v1 | Kitaev states no precision for the Fourier transform itself; your 2(pε′)^{1/2} is your own derivation. See list below. |
| 25 | CW2000 | §7.1 | OK | v1 | A sketch only ("details will appear in the final version"). Approximate, depth O(log n · log log(1/ε)). |
| 26 | IMS2001 | Thm 11, §5 | PARTIAL | v1 | Five of the six attributes check out. See list below. |
| 27 | Trappeniers2024 | Thm 2.3 | OK | v2/v3 (not v1) | Laz and Laz⁻¹ are functorial and mutually inverse. Ex. 2.1 shows p-groups of class k < p are Lazard groups. The subgroup correspondence is Cor 2.4. |
| 28 | Kimmel2017 | App. C, Thms 1, 20 | OK (arXiv v1) | 1608.00281v1 | In the npj version, Thm 20 / App. C becomes Supplementary Thm A3 (§A.1); Thm 1 keeps its number. |
| 29 | Go2025 | Thm 2 | OK | v3 | Thm 2 is the error bound ½‖·‖⋄ ≤ 4t²/n. The sample-count form n ≤ 4t²/ε is Corollary 3. |
| 30 | BeneWatts2026 | Thm 5, Rem 6 | PARTIAL | v1 | Output is a state, not a projector; cost depends on λ_min. See list below. |
| 31 | BeneWatts2026 | Algs 1–2 | OK | v1 | Alg 1 is the "Anti-symmetrization growth measurement"; Alg 2 is the procedure that calls it repeatedly. |
| 32 | Luks1992 | Thm 3.2(5), (7) | PARTIAL | author PDF | (5) is the vector stabilizer, (7) the subspace stabilizer. See list below. |
| 33 | ChildsQA | Thm 5.1 | OK | 17 Apr 2025 | Chapter 5, §5.3: "a deterministic classical computer must make Ω(√N) queries". The proof needs pairwise-trivial intersections (the surrounding text says "trivially intersecting"). Randomized algorithms appear only in a remark. |
| 34 | ChildsQA | Eq. (10.10) | OK | 17 Apr 2025 | k ≥ ⌈2(log N − log ε)/log(1/max F)⌉; F ≤ 1/√2 is (10.24)–(10.26). Your ⌈4 log₂(3r)⌉ is a correct substitution of your own; it is not in the notes. |
| 35 | Ye2021 | Lemma 1 | PARTIAL | v6 | Lemma 1 is specific to rank-k subgroups. See list below. |
| 36 | Nayak2022 | §1 | OK | v3 | Birthday algorithm for Simon's problem, generalized to the HSP (Nayak's HSP is the decision version: is the subgroup trivial?). |
| 37 | Nayak2022 | Cor 4.2 | OK | v3 | "at most 2⌈√(n ln n)⌉ … arbitrary group G with order n". Deterministic and non-adaptive; the query set is shown to exist by a probabilistic argument, not constructed. |
| 38 | EHK2004 | Thm 2 | OK | v1 | s ∈ Θ(n² + log(1/ε)) with n = log\|G\|. The source has a typo, "1 − 1/ε" for 1 − ε. Exponential time is stated in the abstract, not in Thm 2. |
| 39 | Khukhro1998 | Ch. 10 (Chs. 9–10) | PARTIAL | table of contents | Ch. 9 is the Baker–Hausdorff formula; Ch. 10, "The correspondences of A. I. Mal'cev and M. Lazard", has §10.2 on Lazard (p. 121). The subgroup statement was not seen in the book. |
| 40 | LN1997 | Thm 5.41 | PARTIAL | secondary | Three arXiv papers quote it identically, and it matches your sentence. The book itself and the ψ(0)=0 convention were not seen. |

## Items needing a fix
- **8 (PARTIAL).**
  - "HSMC" means *hidden subgroup modulo the commutator* (the subgroup HG′), not "hidden-subgroup-membership". Please rename it.
  - The "at most n² calls" is correct (Prop 1 proof).
  - The ∏_{i=2}^c S(p,n_i) copies (Prop 2 proof) are what one converted copy of the subgroup state of the abelian quotient G/G′ costs. Each HSMC call needs several such copies for the [II22] abelian algorithm, so it uses (number of copies [II22] needs) × ∏S, not ∏S alone.
  - The n_i belong to the lower central series of the semi-elementary quotient, not of G.
  - σ_p is not stated in the source. It follows from inequality (3) at i = ⌊log d₀⌋ together with the ⌈log p⌉ exponent in Prop 5. The source's displayed bound is weaker: its exponent of (n+1) appears as both 2^{⌈log((p−1)/2)⌉} and ⌈(p−1)/2⌉.
  - Your σ_p is independently consistent with KOW Thm 1.8, which gives n^{(q̄/4)·log₂ q̄}. KOW §5.2, by contrast, quotes the weaker n^{⌊q/2⌋⌈log₂ q⌉}.
  - Suggested wording: "the proofs of Props 1, 2, 4, 5 give (our computation) …".
- **10 (PARTIAL).** The exact Watrous method is used to prepare |M₁⟩ for M₁ in a subnormal series. Suggest "uniform superpositions over subgroups".
- **13 (NOT SUPPORTED).** Source: "Imran and Ivanyos [II24] … finding solutions in poly(m) time whenever m ≥ q^{Cq² log q}·n^{⌊q/2⌋·⌈log₂ q⌉}".
  - No version of KOW (v1–v3) gives the q^{q²}(n+1)^{q−1} bound.
  - Suggest citing KOW §5.2 (or Thm 1.8) only for the earlier n^{O(q log q)} bounds, and KMOSW Thm 1.11 alone for the improvement.
- **15 (PARTIAL).**
  - Lemma 3.6 only gives a sparse dependency, using at most ((1−q⁻¹)/(1−q⁻ʳ))ℓ + r vectors.
  - The count (1−q⁻¹)ℓ²/2 + ℓ log_q(ℓ+1) + O(ℓ) is in Remark 3.8 (on Thm 3.7). For q > 3 that result finds a (±⌊q/4⌋)-zero-sum, not a subset sum.
  - For q = 3 the count is Thm 1.2 (n²/3 + Cn log n), proved via Lemma 2.3.
  - Suggest "Lemma 3.6 and Remark 3.8 (for p = 3: Lemma 2.3 and Thm 1.2)". Applying this to κ-th-power equations would be your own adaptation.
- **16 (PARTIAL).** The (d+1)(d+2)/2 count is right, but the algorithm is randomized: "we can easily compute a quadratic non-residue λ in probabilistic polynomial time", and the paper says this is "the only probabilistic part". It is deterministic only under ERH or with a non-residue given. Keep the citation for the count, but do not call Claim 1 deterministic; for a deterministic version, cite Ivanyos–Santha §3.1.
- **21 (UNSURE).** Lemma 12 is a recursion of depth d (ℓ = 1…d). Each step has two levels (E = d^ℓ(m+1) blocks of B_ℓ vectors), indexed by {1…d}^ℓ. The literal two-level "blocks of blocks" (G(d,m)² vectors giving 4 representations) is in the proof of Thm 3, §3.3. Please say which one you mean; if it is the doubling, cite §3.3.
- **22 (PARTIAL).** Fact 2 is stated for a₁x₁^d + … + a_{d+1}x_{d+1}^d = 0, that is, d+1 variables, in deterministic poly(d, log q) time. With j ≤ d variables a nonzero solution may not exist; for example x² + y² = 0 over F_p with p ≡ 3 (mod 4). Change "j ≥ 2" to "j ≥ d+1" (or κ+1).
- **24 (PARTIAL).**
  - §5, Theorem 2 and eq. (25) exist. The construction covers any modulus q (Kitaev assumes 2^{n−1} < q < 2^n "for simplicity").
  - Theorem 2's precision 2(|Ω|ε)^{1/2} is for the reversible eigenvalue measurement Q_q, with |Ω| equal to the modulus. Kitaev never states a precision for V_q.
  - Your 2(pε′)^{1/2} for the transform follows from (25) only if T_q (the creation of |ψ_{q,a}⟩, including the amplitude rotations) is exact, which Kitaev does not state. Present it as your derivation from Thm 2 and (25).
- **26 (PARTIAL).** Unique encoding, time poly(input size + |G′|), arbitrary H and fixed constant error (stated as a convention in §2) all check out. That each group-oracle call counts as one step is never stated; it is only implicit in the oracle model. Present it as the standard black-box convention, not a statement of Thm 11.
- **30 (PARTIAL).**
  - Theorem 5 "returns the unique anti-symmetric state over the support of ρ with probability at least 1 − r(1 − λ_min/r)^n". That is a state, not a projector, and the copy count depends on λ_min (logarithmic in 1/ε).
  - Remark 6 only says the WHILE loop can stop at k < r when the rank is known.
  - Suggest "an anti-symmetric state on the span" and adding the λ_min dependence. Thm 7 / Remark 8 have better copy counts.
- **32 (PARTIAL).**
  - Thm 3.2 runs in time polynomial in n + log|F| + ν, where ν is the largest prime dividing |G| other than the characteristic.
  - The claim holds for p-groups in characteristic p (no other primes). For general solvable matrix groups the "for every N and p" fails without the small-ν hypothesis.
  - The stabilizer under conjugation is (8), the centralizer, for x ∈ GL; or (5) applied to the induced N²-dimensional action.
  - Suggest "Thm 3.2(5), (7), (8), for G of characteristic-p order (more generally when ν is polynomially bounded)".
- **35 (PARTIAL).** Lemma 1: "Any classical randomized algorithm solving GSP(p,n,k) needs Ω(√(p^{n−k})) queries". It is about rank-k subgroups of Z_pⁿ. It matches the "N subgroups that meet only in the identity" form only for k = 1, where the subgroups are lines; say "for Z_pⁿ with k = 1".
- **39 (PARTIAL).** The table of contents confirms the chapters. The subgroup ↔ Lie subring statement and the class < p hypothesis are confirmed only through Bachiller (arXiv 1507.02137v2), who cites "[Khukhro, Chapters 9 and 10]". Google Books returned a CAPTCHA and archive.org is lending-restricted. Keep "class < p" in the sentence; Trappeniers Cor 2.4 is a checkable alternative for the subgroup form.
- **40 (PARTIAL).** The content matches (it is the a = 1 case: monic, positive degree, not an m-th power, d distinct roots, bound (d−1)q^{1/2}), but only through secondary sources. L–N's own ψ(0)=0 convention is not confirmed, and whether the 1983 first edition uses the same number is UNSURE.

## NO ACCESS and unchecked published versions
No source was fully inaccessible. These published versions could not be checked against the arXiv numbering:
- **ISS Algorithmica 2012:** SZTAKI copy restricted.
- **Go et al., QST:** the IOP link returned HTML instead of a PDF.
- **Ye et al., Information and Computation:** ScienceDirect returned 403.
- **IMS SPAA, GKSZ CCC, Cleve–Watrous FOCS, EHK IPL, KOW STOC:** not tried.
- **Khukhro and Lidl–Niederreiter book texts:** not seen (see #39 and #40).
