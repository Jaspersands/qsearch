# Literature priority check: worst-case F_3^n subset sum below n^2/3; nested-dependency technique

Date: 2026-11-08. AI literature pass (arXiv PDFs and API, Semantic Scholar API, web search).
No repository content was sent anywhere; downloads are in the session scratchpad only.
Extends `2026-11-07-rees-sde-subquad-lit.md` and `2026-11-08-rees-sde-lit2.md`; items verified
there are cited, not redone. Notation as in KOW: n = dimension, m = number of vectors.
Labels: [V] read in primary text; [S] secondary only; [I] my inference, not literature.

## Verdict
1. **Worst-case m = n^2/4 + o(n^2), or any constant c < 1/3: NOT found in any source.** The best
   published worst-case bound for F_3^n subset sum is still KOW Theorem 1.2,
   m >= n^2/3 + C n log n [V, v1-v3]. KOW list o(n^2) as open in Sec. 5.1 [V, v1-v3], and their
   Sec. 4.7 "Further optimizations" gives no F_3 improvement [V, v3]. KOMSW (2609.40321) call
   KOW's ~n^2/3 the prior polynomial-time bar. Their only F_3 classical improvement,
   c* = (8 log2 3 - 9)/36 ~ 0.1022, is for the AVERAGE-case Problem 1.1, has no proof, and is
   explicitly LLM-derived [V]. Their worst-case result (Thm 1.11) is q^{q^2}(n+1)^{q-1}, which
   is worse at q = 3 [V, previous pass].
2. **The technique combination is not found.** "Large-weight (about q+2) dependency in a
   q-dimensional quotient whose support carries a nested second dependency, giving 2 dimensions
   per round", "peeling series classes until the dependency code has dual distance >= 3", and
   "second power moment (Pless) variance bound plus conditional expectations for a codeword in a
   weight window" appear in none of KOW, KOMSW, Imran-Ivanyos (II24) or ISS. No other source
   was found either. The nearest published ideas run in a different direction (Sec. 2).
3. **Residual risk.** (a) KOW's STOC 2026 PDF (ACM DOI 10.1145/3798129.3800731) gave HTTP 403,
   not read; [I] arXiv v3 (5 Mar 2026) is probably the camera-ready text. (b) There is
   indexing lag for Sept-Nov 2026; KOMSW has 0 indexed citers. (c) The KOMSW average-case gadgets
   are undisclosed; they might nest dependencies, but claim nothing worst case.

## 1. What each requested source says about worst-case F_3 (KOW notation)

- **KOW, arXiv:2510.07515 v1 (8 Oct 2025), v2, v3 (5 Mar 2026).** [V] Sec. 2 is identical in
  v1 and v3 apart from one remark added in v3 (diff of the extracted Sec. 2 text).
  - Thm 2.1: worst case at m >= (n+1)^2.
  - Thm 2.2: worst case at m >= (n+1)(n+2)/2, a special case of ISS Claim 1. A dependency
    u - u' = 0 makes 0, u and -u all subset sums. Project onto a complement of span(u).
    One dimension per round.
  - Lemma 2.3: given l + t vectors in an l-dimensional space, t = ceil(log3(l+1)), it finds a
    SPARSE zero-sum on at most 2(l+1)/3 + t vectors. Method: first moment over a uniform alpha
    in F_3^t (each coordinate of v_alpha is 0 or uniform), then brute-force enumeration.
  - Thm 1.2: the recursion m_l = m_{l-1} + 2(l+1)/3 + t gives n^2/3 + O(n log n).
    Still one dimension per round; the saving comes only from sparsity.
  - v3 remark after Lemma 2.3, quote: "algorithmizing the Plotkin bound [Plo60], though they are
    stuck at the same 2/3 ratio". The authors therefore considered coding-theoretic
    (first-moment/Plotkin) routes to SPARSE codewords and saw them stall at 2/3.
  - Sec. 3, Lemma 3.6 / Thm 3.7: the F_q generalization; at q = 3 it gives the same 1/3 [V,
    previous pass]. Sec. 4.7: sparsity (r ~ log_q n) and dimension reduction are listed as
    savings for the q >= 5 SIS^infty / CIS / Subset-Sum results only. No F_3 statement.
  - Sec. 5.1, quote: "we ask if it is easy to solve with only m = o(n^2) input vectors".
    Sec. 5.6: "the task becomes easy once m >= n^2/3"; the authors speculate about n^c,
    1 < c < 2. No mention of n^2/4 or of any c < 1/3 anywhere in v1-v3 (grep for 1/4, n2/4,
    quarter, Pless, variance, second moment, dual distance, nested: no hits) [V].
- **KOMSW, arXiv:2609.40321 v1 (30 Sep 2026; only version).** [V]
  - Abstract and Sec. 1.1, Problem 1.1: "given m random vectors"; throughout it is average case.
  - Sec. 1.3: "Prior work [KOW26] gave an efficient classical algorithm that uses m ~ n^2/3
    equations. We improve this to m = c* n^2". The AI disclosure says the GPT-6 interactions
    aimed at "improving the classical algorithm for Problem 1.1", which is the average-case
    problem. No description or proof; "builds on the strategy of [KOW26]".
  - Worst case: grep "worst" finds only Problem 1.9 / Thm 1.11 (general constant q, exponent
    q-1) and Sec. 6. No worst-case F_3 constant below 1/3.
  - [I] c* contains log2 3 = kappa* (Fact 1.2, the average-case information threshold). That
    points to density/collision gadgets that use input randomness.
- **Imran-Ivanyos, arXiv:2304.08376 v1 (only arXiv version; QIP 23:14, 2024).** [V] Thm 2 (and
  Prop. 4 for signed sums) is for constant p with exponent O(p log p); no F_3-specific constant.
  - Concluding remarks: a randomized worst-to-average reduction that turns an average-case
    solver on S vectors into a worst-case solver on (1/delta) S^2 vectors.
  - [I] So the KOMSW average-case c* n^2 transfers to worst case only at order n^4. Average-case
    constants say nothing about worst-case c < 1/3.
- **Ivanyos-Sanselme-Santha (arXiv:0707.1260, Algorithmica 2012).** [V, previous pass] Claim 1:
  (d+1)(d+2)/2 variables for d diagonal quadratic equations, worst case. At p = 3 this is
  KOW Thm 2.2 (~n^2/2). Recursion with one dimension per round; no sparsity or nesting.

## 2. Technique-level comparison

- **Dimension reduction from a dependency**: ISS Claim 1, KOW Thm 2.2 [V]. Always one dimension
  per dependency.
- **Sparse dependency via first moment + enumeration**: KOW Lemma 2.3 / Lemma 3.6 [V]. It
  derandomizes by brute force over F_3^t, t ~ log3 l. Lemma 3.6's general-q proof uses
  conditional expectations [V, previous pass]. Target: LOW weight (<= 2l/3), not a window.
- **Plotkin-bound algorithmization**: mentioned only, said to stall at 2/3 (KOW v3) [V].
- **KOMSW "equation array" (Sec. 6, Lemma 6.1)**: blocks combined by dependencies on lines of
  G^l [V, previous pass]. This is a hypercube of nested dependencies, but it is exponential in q
  and gives (n+1)^2 times 3^9 at q = 3, not a 2-dimensions-per-round gain.
- **Large-weight ternary solutions**: Bricout et al., SAC 2019 (cited by KOW for Wave [V]) is
  exponential-time ISD on random instances [S], not a polynomial worst-case recursion.
- **Not found anywhere**: a large-weight dependency carrying a nested second dependency
  (2 dimensions per round); series-class peeling to dual distance >= 3; a Pless second-moment
  variance bound with conditional expectations to hit a weight window. Pless moments at dual
  distance >= 3 are standard in weight-distribution work [S]; no zero-sum use was found.
- [I] Novelty therefore looks plausible. KOW's v3 Plotkin remark shows that simple moment
  arguments for sparse codewords were tried and stall at 2/3. Any write-up should cite that remark
  and explain why a window plus nesting avoids the stall.

## 3. Citation and recent-work sweep

- Semantic Scholar citers of KOW (2026-11-08): the same 12 as last pass, none algorithmic [V].
- arXiv:2610.00502 v2 (30 Sep 2026), "Quantum Algorithms for OPI Variants Beyond Locality and
  Classical Decodability" [V, PDF grep], cites KOW but is not in the Semantic Scholar list. It
  says the classical algorithms [ISS12, IS15, II24, KOW25] "kick in at the quadratic scale" and
  require "m >= Kn^2 for a constant K". It makes no classical improvement; its quantum results
  target m <= n^{2-Omega(1)} for structured codes.
- arXiv API, Sept-Nov 2026 (title "Subset-Sum"; "binary-error LWE"; "vector subset sum"; "zero
  sum subsequence" + algorithm; "Regev's reduction"; "Chen, Liu, and Zhandry") and web searches
  (n^2/4; zero-sum subsequence F_3^n; ternary quadratic; Pless + conditional expectations; nested
  dependency) [V for listings]: only KOW, KOMSW, II24, integer subset-sum papers (2610.20742,
  2610.31056, ...) and weight-distribution papers. 2503.23238 (Wagner, SIS^infty) is average case.

## 4. Claim gates for the project

- Do not cite KOMSW 0.1022 as a worst-case baseline: it is average case and unproved.
- The worst-case bar to beat is 1/3 (KOW Thm 1.2). A proved worst-case c = 1/4 would be new
  relative to all sources read. Its priority rests on this negative search, not on a proof.
- Cite KOW v3's Plotkin "2/3 ratio" remark as the known limit of the sparse-codeword route.

## Sources (read this pass; copies in the session scratchpad only)

arXiv PDFs 2510.07515v1, v2, v3 (Secs. 1.5, 2, 3, 4.5, 4.7, 5.1-5.6); 2609.40321v1 (Abstract,
Secs. 1.1, 1.3, AI disclosure, "worst" grep); 2304.08376v1 (Thm 2, Sec. 6); 2610.00502v2
(grep). arXiv API listings and abstracts (2610.00502, 2610.31056, 2503.23238). Semantic
Scholar citations API for 2510.07515, 2609.40321 and 2304.08376. Not read: KOW STOC 2026 ACM
PDF (403); BCDL SAC 2019 full text.
