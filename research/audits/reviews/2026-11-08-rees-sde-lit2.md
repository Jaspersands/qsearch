# Literature pass 2: several quadratic forms, diagonal systems, hardness, o(a^2) priority

Date: 2026-11-08. AI literature pass (web search, read-only fetch, pdftotext in the
session scratchpad). No repository content was sent anywhere. Extends
`2026-11-07-rees-sde-subquad-lit.md`; items verified there are not repeated.

Notation: a equations (lambda_i in F_p^a), M variables. KOW/KOMSW write n = a and
m = M. Quadratic-forms papers write r = number of forms, N or n = variables.
Labels: [V] read in primary text; [S] secondary only (source named); [I] my own
inference, not literature, to be checked before use.

## Verdict

1. Item 4 (priority of O(a^2/log a)). No source found states or implies worst-case
   poly time with o(a^2) variables for diagonal quadratic or kappa-th power systems
   at any p. IS 2015 v2 still calls d = 2 "n = Omega(m^2)" [V]; KOW Thm 3.7 saves a
   constant only [V, previous pass]; KOMSW never treats large p with kappa fixed [V];
   Hashimoto's m^2 - 2m^{3/2} is random-only and disputed; Thomae-Wolf is a
   reduction. Theorem A looks new relative to these sources; [I] it is not immediate
   from them (none has a log-saving mechanism).
2. Item 1. For several quadratic forms over F_q, every constructive route found needs
   about r^2 variables or more. Linear-in-r existence bounds are non-constructive
   (counting, Hensel, Nullstellensatz, character sums) and need q or p exponential
   in r (Heath-Brown 4r+1 at q >= (2r)^r; 2Rk+1 at p > k^{2R+2}). Nothing gives
   near-linear M at p = poly(a).
3. Item 2. No new worst-case zero-sum/diagonal algorithm with M = o(a^2) since
   Sept 2026. KOW's recent citers are DQI papers; KOMSW has no indexed citers. The
   KOMSW 0.1022 is for the AVERAGE-case Problem 1.1, mechanism undisclosed ("several
   LLM-constructed gadgets"), no proof [V].
4. Item 3. NO hardness evidence of any kind for worst-case F_3 subset sum with
   m = o(n^2), or for kappa-th powers at constant p with 2n < m < n^2. All proved
   SIS/LWE hardness needs q >= poly(n); the one constant-modulus completeness result
   (SZZ, q = 4) puts the hardness in extra constraint rows; linear-m F_3 subset sums
   are believed hard only conjecturally (Dinur et al., mixed moduli).

## 1. Several quadratic forms; diagonal systems (item 1)

### 1a. Common zeros and common totally isotropic subspaces

- **van de Woestijne**, thesis "Deterministic equation solving over finite fields",
  Leiden 2006 (hdl 1887/4392), and the ISSAC 2005 paper. [V] Theorem A3:
  deterministic poly(n, log q) for (A1) sum_{i=0}^n a_i x_i^n = 0 in n+1 variables
  and (A2) sum a_i x_i^n = b; Thm 1.10: a point on one quadric (odd char). ISSAC
  abstract: any characteristic and any n (no solution need exist if n^2 > |F|). One
  equation only; it is the ISS base case and is uniform in p.
- **Leep-Schmidt**, "Systems of homogeneous equations", Invent. Math. 71 (1983)
  539-549. [V, GDZ scan, OCR] Introduction quotes Leep [Crelle 1984]:
  v_{2,r} <= (1/2) v_2 (r^2+r). Over F_q (v_2 = 2) this means r^2+r+1 variables
  suffice for r GENERAL quadratic forms. p-adic: (3.12p), (3.13p) 2r^2+2r-4. The
  diagonal contraction inequalities (2.11)-(2.12) are multiplicative, so
  exponential in r.
- **Heath-Brown**, survey arXiv:1201.0879. [V] Leep's induction (5):
  beta(r;K,m) <= (r+1)m + beta(r;K) (beta(r;K,m) = largest n with r forms sharing no
  projective m-space); (4): beta(r;K) <= beta(r-k; K, beta(k;K)). Amer's theorem
  (Thm 3) gives beta(2; F_p, m) = 2m+4 for p >= 3. The survey says it is unknown
  whether beta(3; F_p, m) = 2m + O(1).
- **Heath-Brown**, arXiv:0810.1122 (Compositio 2010). [V] Main theorem: r p-adic
  forms with n >= 4r+1 have a common zero if the residue field has q >= (2r)^r;
  Corollary 2: n >= r^2+1 suffices for r >= 5, q >= 4*10^8 r^2. The proof counts
  nonsingular residue-field zeros; it is not constructive.
- **Amer-Brumer** (pencils) [S, via the survey]: q1, q2 have a common zero iff
  q1 + T q2 is isotropic over K(T). Ivanyos-Kutas-Ronyai (arXiv:1610.08671) give
  randomized poly-time zeros of forms in >= 4 variables over F_q(t), odd q [S,
  abstract via search]. [I] Together these plausibly solve r = 2 general forms in
  poly time; nothing found extends to r >= 3.
- **Castel** (ANTS X, 2013) [V, abstract] and **Simon** (Math. Comp. 2005) [S]: one
  form over Q in dimension >= 5. Not about systems.
- [I] The Leep induction as written is exponential: a 3-dimensional space isotropic
  for r-1 forms takes 3 nested (r-1)-form solves, so T(r) = 3 T(r-1). Balanced
  splitting k = r/2 in (4) looks quasi-polynomial in both time and variables.
- [I] For general forms in char != 2 there is a simple poly-time route with O(r^3)
  variables. Choose x_1..x_k in turn, each orthogonal to the earlier ones under all
  r bilinear forms (about r*k variables, linear algebra only); on span(x_j) all forms
  are diagonal; apply ISS with k = (r+1)(r+2)/2. Orientation only.
- Conclusion: no known poly-time algorithm finds a common zero of r general
  quadratic forms over F_q with o(r^2) variables. For diagonal forms, ISS
  (r+1)(r+2)/2 is the best constructive count, uniform in odd p.

### 1b. Systems of diagonal (additive) forms

- **Davenport-Lewis**, Phil. Trans. A 264 (1969). [S: OpenAlex; Cook's restatement
  for odd k is N >= 9 R^2 k log(3Rk)] Quadratic in R. "Notes on congruences III"
  (1966): two additive forms of equal degree have a nonsingular zero mod every prime
  under mild conditions [S, via Knapp].
- **Knapp**, "Pairs of homogeneous additive equations", Theorem 1. [V] Two degree-k
  diagonal forms over F_q, p not dividing k, s >= 2k+1 variables, every nontrivial
  combination with >= k+1 nonzero terms: a nonsingular common zero exists. The proof
  uses Alon's Combinatorial Nullstellensatz; existence only, R = 2. Knapp JAMS 82
  (2007) Thm 2 and "Systems of diagonal forms II" Thm 1 [V]: quadratic in R.
- **Low-Pitman-Wolff** (Wolff, not Wolfson), J. Number Theory 29 (1988) 31-59. [S:
  abstract and Knapp's description] The tool is matroid partitioning: the matrix has
  t disjoint nonsingular R x R minors iff s_m >= t*m for all m. [I] That step is
  algorithmic but only normalizes; it does not produce mod-p zeros. Full text
  blocked.
- **Brudern-Godinho**, BLMS 31 (1999) [S, abstract]: order k^2 in the degree; R^2
  or worse in R for all p.
- **Atkinson-Cook**, J. Austral. MS 46A (1989). [V] Thm 1: two additive equations,
  n > 4k, p > k^6 have a p-adic zero. Their example of R disjoint pairs gives 2Rk
  variables with no p-adic zero for every p = 1 mod k. So 2Rk+1 is a floor for p-adic
  and normalized mod-p methods. Over F_p alone, Chevalley gives Rk+1.
- The only linear-in-R bound found: more than 2Rk variables give a p-adic zero for
  all p > k^{2R+2}. [S: Meir, Mathematika 45 (1998), abstract, citing it as known,
  probably Atkinson-Brudern-Cook 1992; primary not read] With R = a this needs
  log p > ~2a log k. Its method (Hensel, Cauchy-Davenport, character sums) was not
  seen, so constructivity is unknown.
- Conclusion: no diagonal-system existence theorem found has an algorithm. The
  contraction arguments are constructive given a one-equation solver [I], but
  exponential (Leep-Schmidt 2.11-2.12) or quadratic (ISS-type) in R. Linear-in-R
  bounds need p exponential in R.

## 2. Since September 2026; the KOMSW gadget (item 2)

- **KOW citers** (arXiv:2510.07515; Semantic Scholar API, 2026-11-08): 12 in all.
  The two from Sept 2026 on [V, abstracts] are arXiv:2610.01902 (DQI streaming) and
  2609.40036 (cycle codes and DQI). Neither gives a zero-sum, subset-sum or
  diagonal-system algorithm. The older citers (DQI, OPI, Regev reduction) do not
  improve KOW's worst-case m.
- **KOMSW citers** (arXiv:2609.40321): none indexed on 2026-11-08 [V for the API
  result; indexing lag likely]. arXiv API searches (Sept-Nov 2026: binary-error LWE,
  zero-sum, SIS infinity, diagonal equations, Chevalley-Warning, isotropic plus
  algorithm) found no new algorithm. Unread, existence-type by title:
  arXiv:2610.19016 (zero-sum problems of new types), 2610.21577 (skew Combinatorial
  Nullstellensatz, Ax-Katz).
- **KOMSW 0.1022**, v1 Sec. 1.3 eq. (1) and the AI disclosure. [V]
  c* = (8 log 3 - 9)/36 ~ 0.1022 (log base 2). Quoted descriptions: "a convoluted
  affair that builds on the strategy of [KOW26], but uses several LLM-constructed
  gadgets"; the authors "do not give a complete description or formal proof". The
  disclosure says c* was ~0.1069 with GPT 5.6 and then fell "largely through
  improved search capability" with GPT 6. The target is Problem 1.1, the
  AVERAGE-case problem with independent uniform h_i; no worst-case claim.
  [I] The leading constant contains log2(3) = kappa*, the average-case information
  rate (their Fact 1.2). That suggests the gadgets use input randomness (collision
  densities); transfer to worst case is unshown.
- **KOMSW worst case**, Theorem 1.11, Sec. 6, Lemma 6.1. [V] An "equation array":
  blocks of m_l = (q-1)^{l(l-1)/2}(n+1)^l vectors, combined by linear dependencies,
  give disjoint subset sums w_a (a in G^l) with sum_s s w_{a(j<-s)} = 0 on every
  line; at l = q-1 these yield a subset sum. Result: m >= q^{q^2}(n+1)^{q-1}. It
  specializes the IS17 array and is worse than KOW's n^2/3 at q = 3.

## 3. Hardness (item 3)

- **Sotiraki-Zampetakis-Zirdelis**, FOCS 2018, arXiv:1808.06407. [V] cSIS: given
  A in Z_q^{n x m}, a "binary invertible" G in Z_q^{d x m} and b, with q <= 2^l and
  m >= (n+d) l, find x in {0,1}^m with Ax = 0 and Gx = b, or a collision.
  - Thm 4.11: PPP-complete. The gadget is at q = 4 (NAND as x+y+2z-w = 2 mod 4),
    extended to q = 2^l.
  - Thm 5.7: weak-cSIS (b = 0, m > l(n+d)) is PWPP-complete.
  - Open Problem 1.2: "Is SIS or MINKOWSKI PPP-hard?"
  - Constant modulus and linear m, but the hardness sits in G. No prime-q or plain
    zero-sum version.
- **Micciancio-Peikert**, CRYPTO 2013, ePrint 2013/069. [V] Thm 1.2 (from Thm 4.6):
  LWE with uniform {0,1} errors and m = n(1 + Omega(1/log n)) samples is as hard as
  worst-case lattice problems in dimension Theta(n/log n). It needs a prime
  q >= n^{O(1)}; SIS Thm 1.1 needs q >= beta n^delta. Nothing at constant q.
  [I] Dually this is planted subset sum at m ~ n log n and poly q. The kappa-th-power
  coefficient set at large p is dense (size ~ p/kappa), so it does not transfer.
- **Arora-Ge** ICALP 2011 [V]; **ACFFP** hal-01072721 [V]. Binary-error LWE is poly
  time from C(n+2,2) samples (ACFFP Thm 10). Thm 8, under semi-regularity: m = 2n
  gives 2^{0.43 omega n}; m = O(n log log n) gives subexponential time. KOMSW proves
  the full tradeoff unconditionally.
- **Kirchner-Fouque**, CRYPTO 2015, arXiv:1506.02717, Cor. 6 [V]: binary LWE with n
  samples in 2^{(ln2/2 + o(1)) n/log log n}. This needs log q = omega(1); at
  constant q it is 2^{Theta(n)}.
- **Herold-May**, PKC 2017 [S, abstract]: LP solves Galbraith's integer (not mod q)
  vectorial subset sum for m <= 2n.
- **Restricted models**: no SoS, low-degree, SQ, Nullstellensatz or
  polynomial-calculus lower bound found for F_3 subset sum or binary-error LWE at
  constant q. Zadik-Song-Wein-Bruna, arXiv:2112.03898 [V, abstract]: LLL solves
  noiseless planted problems that low-degree and SoS bounds call hard. Such bounds
  would therefore be weak evidence here.
- **Dinur et al.**, CRYPTO 2021, ePrint 2021/885 (Wayback copy) [V]: candidate OWF
  F(x) = B(Ax), A over Z_2, B over Z_3, (n, m, t) = (s, 3.13s, s/log 3). Sec. 4.1:
  inversion is an F_3 subset sum with mod-2 parity constraints at linear m. Hardness
  is conjectured only.
- **After Sept 2026** [V, abstracts]: ePrint 2026/2289 (Chen-Jiang-Wang-Zhang)
  distinguishes binary LWE in exp(O(n/log log n)) with m = ceil(n/log log n) at
  q = n^{a+o(1)}, a > 1/2; arXiv:2610.11254 gives polynomial-modulus attacks. Not
  constant q.
- Conclusion: nothing covers worst-case F_3 with m = o(n^2), kappa-th powers at
  constant p with 2n < m < n^2, or near-linear m at large p. GKSZ PPA_p and Alon's
  q = 2 remark (previous pass) are unchanged. Hardness work could only add a new
  conditional result; there is nothing to "match".

## 4. Is O(a^2/log a) at large p known or immediate? (item 4)

- **Ivanyos-Santha**, arXiv:1503.09016 v2 (TCS 657, 2017). [V] Intro: "the only
  existing result in this direction is the case d = 2 ... when n = Omega(m^2)".
  Prop. 9 is SDE(F_q, (m+1)^2, m, 2), randomized; Thm 3 is
  n > d^{d log d}(m+1)^{d log d}. No log saving.
- **Ivanyos-Prakash-Santha**, ESA 2018, arXiv:1806.09660. [V] Learning from subsets
  and hidden multiple shift by linearization (Thm 1.3, (n+d)^{O(d)} samples). No SDE
  bound.
- KOW Thm 3.7 / Rem. 3.8 [V, previous pass]: ((1-1/q)/2) l^2 + O(l log l) for signed
  zero-sums; the constant tends to 1/2.
- Hashimoto 2010 Alg. 1 (m^2 - 2m^{3/2}, random, disputed), MHT (m(m+3)/2), CHMT14
  (~m^2/2), Thomae-Wolf (reduction to M - floor(N/M) + 1 equations) [as in the
  previous pass]: none is worst case, diagonal-specific, or o(m^2). KOMSW [V]: worst
  case only for kappa = q-1 at constant q.
- Verdict: not in these sources. [I] Not immediate either: the known recursions
  spend Theta(l) fresh vectors per dimension, so a log saving needs a new idea such
  as reuse across dimensions or Theorem A's flat/Rado step. Residual risk: the
  unread full texts of CHMT14 and Hashimoto ePrint 2021/1045, both random-system.

## 5. What could change the attacks

- (i) Uniform in p / small fixed p. ISS (a+1)(a+2)/2 is already uniform in odd p,
  since van de Woestijne is [V]. So the real target is o(a^2) at small p. For
  kappa = p-1 the worst-case best is KOMSW Thm 1.11 [V]. Davenport-Lewis-type
  contraction is exponential in R [V for the inequality; I for constructivity].
- (ii) Near-linear M at large p. Linear-in-R theorems need p >= (2r)^r or
  k^{2R+2} and are non-constructive [V Heath-Brown; S the 2Rk bound]. The
  Atkinson-Cook example puts a 2Rk floor under any method that also yields p-adic
  zeros [V]. [I] That p-adic floor does not bind the F_p-only problem, whose
  existence threshold is Rk+1.
- (iii) p = 3. The KOMSW 0.1022 is average-case and undisclosed [V], so it is no
  worst-case baseline. KOW's 1/3 is the worst-case bar [V]. No hardness obstacle to
  o(n^2) exists in the sources read. Dinur et al. is the nearest believed-hard
  linear-m relative, and only with added parity structure [V].

## Sources (read this pass; copies in the session scratchpad only)

arXiv 2609.40321 (Sec. 1.3, 6, AI disclosure), 1503.09016v2, 1806.09660, 1201.0879,
0810.1122, 1808.06407, 1506.02717; abstracts of 2112.03898, 2610.01902, 2609.40036.
hdl.handle.net/1887/4392; vdW ISSAC 2005; GDZ PPN356556735_0071 (Leep-Schmidt);
Knapp (pairs; JAMS 2007; Systems II); Atkinson-Cook 1989; cpeikert LWsE.pdf (MP13);
rongge LPSN.pdf (Arora-Ge); hal-01072721 (ACFFP); ePrint 2021/885 (Wayback),
2026/2289 (abstract); Semantic Scholar citations API. Not read (paywalled or blocked):
Low-Pitman-Wolff, Davenport-Lewis 1969, Atkinson-Brudern-Cook 1992, Meir 1998,
Herold-May, CHMT14 full texts.
