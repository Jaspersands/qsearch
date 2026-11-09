# Literature search: worst-case poly-time zeros of diagonal systems with n = o(m^2) variables

Date: 2026-11-07. AI literature pass (web search and fetch, plus local pdftotext of arXiv PDFs). No repository content was sent out. Notation: n = number of variables, m = number of equations, as in the question. NOTE: Kothari-O'Donnell-Wu (KOW) use the opposite convention (n = dimension = number of equations, m = number of vectors = number of variables); translations are given where it matters.

Labels: [V] = [literature, verified from primary source: abstract or PDF text read]. [S] = [literature, secondary only].
Raw PDF text was read from the arXiv PDFs saved in the session scratchpad; nothing is kept in the repo except this file.

## Bottom line

- No known classical algorithm achieves worst-case o(m^2) variables for fixed d >= 2 and large p for every coefficient matrix. Every verified worst-case result is Theta(m^2) or worse in the number of variables. [V]
- The best known polynomial in m for d = 2 and large p is still Ivanyos-Sanselme-Santha (ISS) Claim 1: n = (m+1)(m+2)/2 (deterministic given van de Woestijne's solver). Ivanyos-Santha (IS) 2015 for d = 2 gives only (m+1)^2 randomized for the warm-up and a weaker exponent for the general theorem. [V]
- The authors of the strongest recent papers explicitly list o(n^2) as OPEN for the simplest case F_3 subset-sum (KOW 2026 sec. 5.1: "we ask if it is easy to solve with only m = o(n^2) input vectors"). [V]
- The best improvement since 2015 is only a constant factor, and only for F_3 (and only average-case in the newest paper): 1/2 -> 1/3 (KOW, worst case) -> 0.1022 (KOMSW 2026, stated for the average-case problem, no proof given). All are still Theta(n^2). [V]

## 1. Verified items, ranked by relevance to "worst-case o(m^2) poly-time"

### 1.1 KOW 2026 and its direct sequel (most important)

KOW: arXiv:2510.07515, Robin Kothari, Ryan O'Donnell, Kewen Wu, "No exponential quantum speedup for SIS^infty anymore". Exists. v1 8 Oct 2025, v3 5 Mar 2026 (quant-ph). The sequel cites it as "STOC 2026" [V, from the sequel's abstract]. [V]

What I could confirm from the v3 PDF text (and the theorem numbers are the same in v1, v2, v3):

- Theorem 2.2 (verbatim substance): "The worst-case F_3^n-Subset-Sum problem can be solved in deterministic poly(m) time when m >= (n+1)(n+2)/2." It is stated as a special case of [ISS07, Claim 1], with a short proof (take l+1 vectors, get a dependency u - u' = 0, so -u is also a subset sum; project the rest onto a complement of span(u); induct on dimension). [V]
- Theorem 1.2: worst-case F_3^n-Subset-Sum, deterministic poly(m), when m >= n^2/3 + C n log n. Proved in Section 2 using Lemma 2.3 (a sparse dependency, support at most 2(l+1)/3 + t, t = ceil(log_3(l+1))) and the recursion m_l = max{l, m_{l-1} + 2(l+1)/3 + ceil(log_3(l+1))}. [V]
- Lemma 3.6 (statement): Let r >= 1. Given l + r vectors in a subspace of F_q^n of dimension l, one can find in deterministic poly(n, r, log q) time a nontrivial (+-floor(q/2))-zero-sum (every coefficient in {-floor(q/2),...,floor(q/2)}, i.e. any nonzero F_q combination) using at most ((1 - q^{-1})/(1 - q^{-r})) * l + r vectors. Proof: expectation argument over beta in F_q^r \ {0} plus derandomization by conditional expectations. [V]
- The project's "(1-1/p) m^2/2 + O(m log m)" is Theorem 3.7 / Remark 3.8: with r_i = ceil(log_q(i+1)), m_l <= ((1-q^{-1})/2) l^2 + l log_q(l+1) + O(l). CAVEAT: Theorem 3.7 outputs a nontrivial (+-floor(q/4))-zero-sum (requires q > 3), a small-integer-coefficient zero-sum, NOT a subset sum with coefficients in {0,1} and NOT a diagonal d-th power solution. For q = 3 it specializes to Theorem 1.2 (coefficient (1-1/3)/2 = 1/3). [V]
- Section 5.1 (open problem, quote-level): "for the F_3^n-Subset-Sum problem, we ask if it is easy to solve with only m = o(n^2) input vectors." [V]
- Section 5.3: "our efficient classical algorithms do not seem to be able to get off the ground unless m >= Omega(n^2)." [V]
- Section 5.2 credits ISS07 (diagonal quadratic, m >= (n+1)(n+2)/2), IS17 (diagonal d-th powers, m >= d^{d(d-1)ceil(log2(d+1))/2}(n+1)^{d ceil(log2(d+1))}) and Imran-Ivanyos [II24] for F_q^n-Subset-Sum. [V]
- Scope caveat for the project: KOW's CIS results (allowed set A of size q-k+1) are average-case and need |A| close to q. For A = d-th powers, |A| = (q-1)/d + 1, so they do not apply. The SIS^infty worst-case result (Theorem 1.5, m >= C n^k, s = floor(q/(2k))) is a different problem (small-integer-coefficient zero-sums), not diagonal d-th power systems. [V]

KOMSW: arXiv:2609.40321, Robin Kothari, Tony Metger, Ryan O'Donnell, Noah Shutty, Kewen Wu, "Exponential quantum speedup for F_3^n-Subset-Sum? Or, rigorous classical algorithms for Binary-Error LWE", 30 Sep 2026 (quant-ph, cs.CR, cs.DS). Exists. [V]

- Quantum, average case: polynomial time for m = eps * n^2 for every fixed eps > 0, and tradeoff time (m/n)^{O(ceil(n^2/m))} for m >= kappa n, kappa > log 3 (Theorem 1.3, Corollary 1.4: quasipolynomial for m >= n^2/polylog n; subexponential 2^{O(n^{1-alpha})} for m >= n^{1+alpha} log n). The same tradeoff holds for a deterministic classical binary-error LWE decoder (Theorem 1.7), but the subset-sum reduction to LWE decoding is quantum. [V]
- Classical F_3 subset sum: improves m ~ n^2/3 to m = c* n^2, c* = (8 log 3 - 9)/36 ~ 0.1022. This is stated under the average-case Problem 1.1; the paper says the algorithm is "convoluted", built from LLM-constructed gadgets, and gives no complete description or proof. Not a verified result and not worst case. The authors say a classical algorithm for every fixed c > 0 "seems to require substantially new ideas". [V]
- Worst-case F_q^n-Subset-Sum, constant q (Theorem 1.11): m >= q^{q^2} (n+1)^{q-1}, deterministic poly(m). Improves the n^{O(q log q)} bound of IS17/II24. This is the kappa = d = q-1 case for CONSTANT q; exponent q-1 grows with q, so it is no help for large p with d fixed. For q = 3 it gives ~3^9 (n+1)^2, which is worse than Theorem 1.2. [V]
- Average-case F_q^n-Subset-Sum (Theorem 1.10): m >= q^{q^2} n^{1+floor((q+3)/4)}. Average case only. [V]
- For m = Theta(n) all known attacks are exponential; Wagner/BKW-type time 2^{O(n/log(m/n))} for larger m. [V]

### 1.2 Ivanyos-Santha 2015 (the project's baseline)

arXiv:1503.09016, Gabor Ivanyos and Miklos Santha, "On solving systems of diagonal polynomial equations over finite fields" (arXiv v1 title; v2 retitled "Solving systems of diagonal polynomial equations over finite fields", v2 8 Jun 2016). TCS (2016), DOI 10.1016/j.tcs.2016.04.045; FAW 2015 LNCS 9130 pp. 125-137. [V, abstract and PDF]

- Theorem 3: for constant d and n > d^{d^2 log d} (m+1)^{d log d} (my reading of the PDF text; superscripts were flattened by pdftotext; KOW's rendering is d^{d(d-1)ceil(log2(d+1))/2}(m+1)^{d ceil(log2(d+1))}), SDE(F_q, n, m, d) is solvable in time poly(n, log q). Requires d | q-1 (the d-th-power structure) and works for every coefficient matrix. The d = q-1 case is the vector zero-sum problem. [V]
- Proposition 9 (quadratic warm-up): SDE(F_q, (m+1)^2, m, 2) solved by a randomized algorithm in poly(log q, m); randomization only to find a non-square (deterministic under ERH; Section 3 removes the need for nonresidues in the general theorem). [V]
- Intro statement of the state of the art: for d = 2 the previous result is ISS "n = Omega(m^2)", and "the case when d is fixed and m grows appears to be more difficult"; for n >= (d+1)m and fixed m the recursion via van de Woestijne is poly in n. Chevalley-Warning gives existence for n > dm. For q = 2, finding a second solution is in PPA and Alon's result implies a poly-time algorithm would contradict one-way permutations (stated there as a motivation). [V]
- Also: deciding existence of a nontrivial 0-1 solution of a linear system over F_q is NP-hard for q >= 3 (SAT reduction). [V]
- Does NOT beat (m+1)(m+2)/2 for d = 2; for d >= 3 the exponent d ceil(log2(d+1)) >= 4 is far above 2. [V]

### 1.3 ISS original source of Claim 1

arXiv:0707.1260v1, Gabor Ivanyos, Luc Sanselme, Miklos Santha, "An efficient quantum algorithm for the hidden subgroup problem in nil-2 groups" (Algorithmica 62 (2012) 480-498). Claim 1 (section 5): "If n' = (d+1)(d+2)/2 then we can find a nontrivial solution for (3) in polynomial time", where (3) is d homogeneous diagonal quadratic equations sum_i u_{l,i} j_i^2 = 0 over F_p; proof is a recursion using van de Woestijne's solver for the 3-variable one-equation case (Theorem A3 of the thesis; deterministic poly(log p)). Here d = number of equations, n' = number of variables. Every coefficient matrix (the u's are arbitrary). The same paper's Theorem 5 handles the combined quadratic+linear system with n = (d+1)^2(d+2)/2 variables. The earlier STACS 2007 paper (arXiv quant-ph/0701235) is the extraspecial-group precursor; the KOW "[ISS07]" label points to the same line of work. I verified Claim 1 in the 0707.1260 text; I did not verify that the STACS version states the identical claim. [V for 0707.1260; the "[ISS07]" attribution in KOW not further resolved]

### 1.4 Imran-Ivanyos zero-sum subsequences

arXiv:2304.08376, Muhammad Imran and Gabor Ivanyos, "Zero sum subsequences and hidden subgroups" (v1 17 Apr 2023; Quantum Inf. Process. 23(1):14 (2024) per DBLP [S for the venue]). [V for arXiv v1 text] Deterministic algorithm for nontrivial zero-sum subsequences in F_p^n for constant p: Theorem 2 in v1 gives S(p,n) = p^{O(p log^2 p)} n^{O(p log p)} vectors; Proposition 4 gives a signed-sum version p^{O(p log p)} n^{O(p)}. The "halving trick" is theirs. This is the kappa = p-1 case with n >> m^2 for p >= 5; no help for o(m^2). KOW report the exponent as n^{(q-bar/4) log q-bar} in the published form. [V]

### 1.5 Underdetermined MQ (general quadratics): all need n of order m^2/2 or more

None of these is for diagonal systems specifically, and none is shown to work for every coefficient matrix; they are designed for (and analyzed on) random/generic systems in cryptanalysis. None goes below ~m^2/2.

- Kipnis-Patarin-Goubin (KPG), EUROCRYPT'99, LNCS 1592 pp. 206-222, DOI 10.1007/3-540-48910-X_15, "Unbalanced Oil and Vinegar Signature Schemes". The usable statement "polynomial time when n >= m(m+1) in even characteristic" is quoted from the abstracts of Hashimoto (ACNS 2010 industrial track, eprint 2009/154) and MHT (IEICE E97.A 2014). The KPG paper itself was not opened. [S for the KPG threshold; V for what those two abstracts say]
- Courtois-Goubin-Meier-Tacier (PKC 2002) odd characteristic: per Huang-Bao, n ~ 2^{m/7}(m+1) and exponential in m. [S]
- Hashimoto, "Algorithms to solve massively under-defined systems of multivariate quadratic equations", ACNS 2010 (eprint 2009/154). Algorithm 1: n about m^2 - 2m^{3/2} + 2m, any finite field, poly time (abstract; note it is for "random" systems). Algorithm 2: n > m(m+1)/2 + 1, exponential time. Huang-Bao (unrefereed arXiv) say MHT pointed out Algorithm 1 does not work efficiently as claimed; unresolved. [V for abstract; S for the rebuttal]
- Miura-Hashimoto-Takagi (MHT), "Extended algorithm for solving underdefined multivariate quadratic equations", IEICE Trans. Fundamentals E97.A(6):1418-1425 (2014) (PQCrypto 2013 version pp. 118-135): polynomial time when n >= m(m+3)/2, even characteristic (Magma test m = 28, n = 504). [V, abstract]
- Cheng-Hashimoto-Miura-Takagi (CHMT14), PQCrypto 2014, LNCS 8772 pp. 40-58, DOI 10.1007/978-3-319-11659-4_3, "A polynomial-time algorithm for solving a class of underdetermined multivariate quadratic equations over fields of odd characteristics". Abstract (Chang Gung Univ. repository page): extends MHT to odd characteristic, widens the range at essentially no cost, and claims running time polynomial in numbers of equations and variables for "polynomially underdetermined" systems. The exact range (the project's "n >= m(m+1)/2") was NOT confirmed from the paper (Springer paywalled). Briaud-Ghosal-Jain-Lou-Sahai (arXiv:2411.14697) describe MHT13 and CHMT14 as polynomial-time algorithms that "require a number of variables roughly quadratic in" the number of equations [V for that sentence]. Huang-Bao's Table 2 says "exp." for odd characteristic for the whole family; there is a source conflict on whether the odd-characteristic version is polynomial in m, unresolved. [S for the exact threshold]
- Huang-Bao, arXiv:1507.03674, "Algorithm for solving massively underdefined systems of MQ equations over finite fields": n >= m(m+1)/2, guess-and-determine, complexity O(q n^omega m (log q)^2) for even characteristic and O(q 2^m n^omega m (log q)^2) for odd characteristic (their text prints q^{2m}-style factor; PDF extraction is ambiguous). Exponential in m for odd characteristic, so not a polynomial algorithm there. Unrefereed. [V as a statement of what the preprint claims; not independently checked]
- Thomae-Wolf, PKC 2012, LNCS 7293 pp. 156-171, "Solving Underdetermined Systems of Multivariate Quadratic Equations Revisited": reduces an MQ system with M equations in N > M variables to one with M - floor(N/M) + 1 equations (same number of variables); it is a reduction, not a poly-time solver. Even characteristic in the original per a 2026 ePrint summary, extended to arbitrary q by CHMT14. I could not open the paper (the Bochum host had a bad certificate; Springer paywalled). The M - floor(N/M) + 1 formula is confirmed by Briaud et al. [V for the formula as stated in arXiv:2411.14697; S otherwise]
- Furue-Nakamura-Takagi (FNT21), PQCrypto 2021, "Improving Thomae-Wolf algorithm for solving underdetermined multivariate quadratic polynomial problem": hybrid guess + Thomae-Wolf; exponential-time improvement, not a poly-time threshold change. Only slides summaries and citations seen. [S]
- Hashimoto, "An improvement of algorithms to solve under-defined systems of multivariate quadratic equations", JSIAM Letters 15 (2023) 53-56; also ePrint 2021/1045. This is an ORIGINAL algorithm paper (not a survey) for fewer variables than earlier methods, with MAYO security analysis; the abstract gives no explicit n-vs-m bound. I found no 2023 Hashimoto survey on underdetermined MQ. [V for abstract of the JSIAM page; eprint full text returned 403]
- Asanuma-Chen-Furue-Sakata-Takagi, eprint 2026/1054, "Improved Complexity Estimates for Underdetermined MQ Systems via Generalized Variable Partitioning": generalizes Hashimoto's partition method; exponential-time improvements for MAYO/QR-UOV/SNOVA parameters (MAYO1 2^156 -> 2^145). Applicability condition is only n > m on the abstract page. [V for abstract]
- Briaud-Ghosal-Jain-Lou-Sahai, arXiv:2411.14697 (22 Nov 2024), "Quantum Advantage via Solving Multivariate Quadratics": quantum poly-time algorithm for a structured distribution of m < n quadratic systems over F_2 (n^2 equations in alpha n^3 unknowns), with a classical-hardness conjecture and a review of Thomae-Wolf/FNT/Hashimoto/Groebner attacks. Not diagonal, not F_p large, not worst case; relevant only as evidence that generic MQ in the m^2 regime is believed classically exponential beyond MHT/CHMT14's range. [V]

## 2. Constructive zero-sum results (kappa = p - 1 and p = 3 cases)

- Existence: Olson / van Emde Boas-Kruyswijk: every sequence of more than (q-1) n vectors in F_q^n has a nonempty zero-sum subsequence (Davenport constant); for q-group case tight (cited as Fact 5.2 in KOW). Existence at n >= dm+1 for diagonal d-th power systems is Chevalley-Warning. Constructive thresholds above sit between about m^2/3 (p = 3) and m^{p-1} (constant p >= 5), far above the existence thresholds 2m (p = 3) and (p-1)m. [V]
- p = 3 (F_3 subset sum): worst case m >= n^2/3 + O(n log n) (KOW Theorem 1.2); average case m ~ 0.1022 n^2 (KOMSW, unproved) classical, m = eps n^2 any eps quantum (KOMSW). Wave signature (DST19) and related are at m ~ 2n (not reached). [V]
- Constant p >= 5, worst case: exponent p - 1 (KOMSW Theorem 1.11). Large p with d = p - 1: nothing polynomial in m known (the exponent depends on p). [V]
- Davenport-style tight sequences are not what blocks the algorithms: the barrier is the use of ~m dependency vectors per dimension reduction step (ISS recursion), giving Theta(m^2).

## 3. Hardness evidence for worst-case n = o(m^2)

I found no reduction, cryptographic assumption, or lower bound for restricted algorithm classes that says worst-case solving with n = o(m^2) is hard for these problems. What exists is weaker:

- Totality/TFNP: for n > dm the problem is total (Chevalley-Warning), so it cannot be NP-hard unless NP = coNP; for q = 2 it is in PPA and IS cite Alon (poly algorithm would imply no one-way permutations). Goos-Kamath-Sotiraki-Zampetakis, arXiv:1912.04467 (CCC 2020): an explicit Chevalley-Warning search problem WITH SYMMETRY (general polynomials, not diagonal, up to constants in the symbols) is PPA_p-complete; BIS_p and SIS^infty_p (x in {0,1}^n resp. {-1,0,1}^n, Ax = b mod p) Karp-reduce to Chevalley_p, BIS_q and SIS_q^infty are in PPA_q, SIS in PPP when n > m log2 q, and Gaussian elimination solves BIS_2 and SIS_p^infty for p in {2,3}. This places the zero-sum problems in TFNP classes but gives no hardness for diagonal d-th power systems and no lower bound at n = o(m^2). [V]
- NP-hardness below the existence threshold: IS state NP-hardness of nontrivial 0-1 solutions for q >= 3 (no totality there). [V]
- Average-case heuristics only: for m = Theta(n) KOMSW and KOW report all known attacks exponential (Wagner/BKW 2^{O(n/log(m/n))}); KOMSW give quantum and classical-LWE-decoder tradeoffs; both note that a classical polynomial algorithm for every fixed constant in m = c n^2 would be new. The m ~ n^2 threshold is the observed barrier of the dependency-recursion method, not a proved boundary. [V]
- Briaud et al. conjecture classical hardness of a structured MQ family over F_2; irrelevant to worst-case large-p diagonal systems. [V]
- DQI/OPI/Yamakawa-Zhandry: KOW sec. 5.3 notes these problems have m = O(n) (dimension n), where "our efficient classical algorithms do not seem to be able to get off the ground". That is a hint that the hard regime for dequantization is m << n^2, not evidence of hardness for diagonal systems. [V]

## 4. KOW 2026 citation verification summary

- arXiv:2510.07515 exists: title "No exponential quantum speedup for SIS^infty anymore", authors Robin Kothari, Ryan O'Donnell, Kewen Wu; v1 8 Oct 2025, v2, v3 5 Mar 2026; category quant-ph; the sequel (arXiv:2609.40321) cites it as STOC 2026. I could not independently confirm the STOC 2026 acceptance beyond that sentence. [V for arXiv listing and PDF; S for STOC]
- Theorem 2.2 is exactly as in section 1.1 above (worst-case F_3 subset sum, deterministic poly(m), m >= (n+1)(n+2)/2, a special case of [ISS07, Claim 1]). Confirmed identical numbering in v1, v2 and v3. The project can drop "NEEDS HUMAN VERIFICATION" for the statement, keeping a note that the notation is swapped (KOW n = project m). [V]
- Lemma 3.6 is not titled "sparse dependencies" in the paper; it is the F_q generalization of Lemma 2.3 (sparse dependency, support at most ((1-q^{-1})/(1-q^{-r})) l + r). The paper does call this a "sparser zero-sum" / sparse linear dependence step (sec. 3.1 and 4.1). Its output is a (+-floor(q/2))-zero-sum, i.e. any nonzero F_q-combination; the diagonal d-th power structure is not addressed. [V]
- The "(1-1/p) m^2/2 + O(m log m)" bound is Remark 3.8 after Theorem 3.7 and is for (+-floor(q/4))-zero-sums for q > 3, not for diagonal d-th power systems or subset sums over F_p with p > 3. [V]
- What I cannot confirm: that the published STOC version has the same numbering as arXiv v3; the (1-1/p)/2 constant as a bound for any diagonal system with d >= 2 and p > 3 (not proved there). [cannot confirm]

## 5. Observation for the project (not literature)

An unverified remark, my own, to be checked before any use: Lemma 3.6's sparse-dependency idea could in principle replace the "l+1 vectors per dimension" step in the ISS d = 2 recursion by "about (1-1/p) l + r vectors", plausibly improving the leading constant (m+1)(m+2)/2 to about (1-1/p)m^2/2 for d = 2 and large p, still Theta(m^2). The residue/nonresidue splitting of coefficients (ISS Claim 1 via van de Woestijne) would need to survive the sparse support. I have not verified this and it does not give o(m^2).

## 6. Sources

- https://arxiv.org/abs/2510.07515 (KOW, PDF read v1, v2, v3)
- https://arxiv.org/abs/2609.40321 (KOMSW, PDF read)
- https://arxiv.org/abs/1503.09016 (Ivanyos-Santha, PDF read)
- https://arxiv.org/abs/0707.1260 (ISS, PDF read)
- https://arxiv.org/abs/2304.08376 (Imran-Ivanyos, PDF read)
- https://arxiv.org/abs/1912.04467 (GKSZ, PDF read)
- https://arxiv.org/abs/2411.14697 (Briaud et al., PDF read)
- https://arxiv.org/abs/1507.03674 (Huang-Bao, PDF read)
- https://eprint.iacr.org/2009/154 (Hashimoto 2010 abstract page)
- https://www.jstage.jst.go.jp/article/transfun/E97.A/6/E97.A_1418/_article/-char/ja (MHT abstract)
- https://pure.lib.cgu.edu.tw/en/publications/a-polynomial-time-algorithm-for-solving-a-class-of-underdetermine-3/ (CHMT14 abstract)
- https://www.jstage.jst.go.jp/article/jsiaml/15/0/15_53/_article (Hashimoto JSIAM Letters 2023 abstract)
- https://eprint.iacr.org/2026/1054 (Asanuma et al. abstract)
- Not opened (paywalled or blocked): KPG99 (doi 10.1007/3-540-48910-X_15), Thomae-Wolf 2012 (doi 10.1007/978-3-642-30057-8_10), CHMT14 full text (doi 10.1007/978-3-319-11659-4_3), FNT21 full text, Hashimoto eprint 2021/1045 full text.
