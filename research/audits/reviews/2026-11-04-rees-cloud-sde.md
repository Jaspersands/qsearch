# Rees HSP cloud research session: sde

- Session: `session_01B1JoCgVr4ufcSUoZpvsgRm` (Claude Code cloud session)
- Started: 2026-11-03T22:54Z; final result event: 2026-11-03T23:36Z
- Task: Find an o(a^2)-column solver for the kappa-th-power (SDE) equation problem, or a hardness result.
- Harvested 2026-11-05 from the session's single `result` event via the claude.ai events API.
  Body below is verbatim (SHA-256 of body: `270adc0ac81afa07aad9782c860dc26dbe8414203da85f6d740dbe53a126f46a`, 15834 chars).
- Status: AI-generated, AI-checked only, pending human review. All Rees claim gates stay false.
- Comparison with the paper: `2026-11-04-rees-cloud-research-harvest.md`.

---

# Power-equation solver below a²: research report

**Problem.** Fix κ ≥ 2 with κ | p−1. Let H = (F_p^*)^κ and P = H ∪ {0}. Given columns λ_1..λ_M ∈ F_p^a, find x ∈ P^M with x ≠ 0 and Σ x_i λ_i = 0. The regime is fixed κ (2 or 3) and growing p. Write K = ker Λ, a subspace of dimension M−a.

**Labels.** *Proved* means a complete argument is given here or in a cited theorem I read. *Experiment* means computed in this session, on finite cases only, so it can only falsify. *Argued* means a heuristic or structural argument, not a proof. *Not checked* means cited from memory or from an abstract only.

Nothing was written to the repository; `git status` is clean. All scripts and logs are in `/root/work/exp/`, inside the cloud container, which is temporary.

---

## 1. Verdict

1. **No polynomial-time algorithm with M = o(a²) was found**, either worst-case or on random columns. At large p even a constant below 1/2 is open: I found no polynomial-time solver using c·a² columns with c < 1/2. The best polynomial-time count is still the triangular (a+1)(a+2)/2, minus a lower-order Θ(a log a) saving (§3).
2. **No reduction from a standard problem at fixed κ and large p was found.** I proved three obstructions that explain why the obvious reductions fail (§4.1–4.3). I also proved an exact equivalence at the bottom of the range, M = a+2, with a power-residue "pattern" problem related to the Legendre PRF. That problem is not a standard assumption, and M = a+2 is far below κa+1.
3. **Every route on your list is blocked at fixed κ and large p.** Lattices, Kirchner–Fouque/BKW, Ducas–Espitau–Postlethwaite, Bai–Galbraith–Li–Sheffield, Weil descent, the norm map, Gröbner bases and Regev/CLZ-style quantum decoding all fail. For three of them the reason is proved: Regev/CLZ (Tao's uncertainty principle), the KOW long-AP machinery (Pólya–Vinogradov) and Gröbner bases (experiment). The rest are argued (§5).
4. **New, but only constant- or lower-order.** Two explicit tradeoffs go below a²/2 at exponential cost; one is proved, one is heuristic plus experiment. In polynomial time they reach M = a²/2 − Θ(a log a), which is not o(a²). The paper's quadratic schedule stands. My evidence supports it only as "best known", not as a proved necessity.

---

## 2. Literature anchors (read in this session unless marked)

- **Ivanyos–Santha, TCS 2017 (arXiv 1503.09016v2).**
  - Theorem 3: polynomial time for n > d^{d² log d}(m+1)^{d log d}.
  - Proposition 9: (m+1)² vectors for d=2, randomized. This is your two-level scheme.
  - The introduction notes that recursion gives (d+1)^m, and that the ISS07 result for d=2 needs Ω(m²).
- **Kothari–O'Donnell–Wu, "No exponential quantum speedup for SIS∞ anymore", STOC 2026 (arXiv 2510.07515v3).** This is the most relevant prior art.
  - At p=3, κ=2 we have P = {0,1}, so **our problem is exactly F_3^n-Subset-Sum**.
  - Theorem 2.2: (n+1)(n+2)/2. It is a special case of ISS07 Claim 1 and is your triangular scheme.
  - Lemma 2.3 and Theorem 1.2 get n²/3 + Cn log n by finding *sparse* zero-sums. The trick depends on F_3: random F_3 codewords have only 2/3 of their entries nonzero. Over large F_p the fraction is 1−1/p, which gives your (1−1/p)a²/2 variant.
  - Corollary 3.15 and Theorem 3.17 handle constrained-coefficient (CIS) sets containing long arithmetic progressions.
  - §5.2 states that ISS07 handles A = quadratic residues at (n+1)(n+2)/2.
  - §5.3 says their classical algorithms "do not seem to be able to get off the ground unless m ≥ Ω(n²)".
- **Kothari–Metger–O'Donnell–Shutty–Wu (arXiv 2609.40321v1).**
  - Theorem 1.3 and Corollary 1.4: a *quantum* polynomial-time algorithm for F_3-subset-sum at m = ε·n² for every fixed ε > 0, via Regev's reduction and a binary-error LWE decoder (Theorem 1.7).
  - A classical algorithm at c⋆ = (8 log 3 − 9)/36 ≈ 0.1022·n², with no proof, built from LLM-found gadgets (§1.3).
  - Theorems 1.10 and 1.11 cover F_q-subset-sum; the exponent of n grows with q.
  - For m = Θ(n), every known attack is exponential (§1.1, §1.2).
- **Underdetermined MQ** (κ=2 is diagonal MQ).
  - Huang–Bao (arXiv 1507.03674), Theorem 3.1: n ≥ m(m+1)/2. Theorem 3.2: in odd characteristic the cost has a 2^m factor, because the last step needs m values to all be squares. That last step is our problem with a = m and M = m.
  - Thomae–Wolf (PKC 2012), Cheng–Hashimoto–Miura–Takagi (PQCrypto 2014), Furue–Nakamura–Takagi (PQCrypto 2021), Hashimoto (ePrint 2021/1045), Asanuma et al. (ePrint 2026/1054): *not checked*. The ePrint PDFs were behind a Cloudflare check. All of these sit at the ~m²/2 frontier.
- **Kirchner–Fouque, CRYPTO 2015 (arXiv 1506.02717).** Theorems 4–5 (BKW with quantization for bounded secrets) and Theorem 14 (low-density subset sum). Both concern *small-norm* coefficient sets.
- **Ducas–Espitau–Postlethwaite, CRYPTO 2023.** Introduction read: an ISIS attack for small q using the geometry of BKZ-reduced q-ary bases (ℓ₂ norm).
- **Bai–Galbraith–Li–Sheffield, J. Cryptol. 2019.** Abstract only: Camion–Patarin/Wagner, HGJ and BCJ for ISIS with small coefficients.
- **Tao, "An uncertainty principle for cyclic groups of prime order", Math. Res. Lett. 12 (2005).** For nonzero f on Z/p, |supp f| + |supp f̂| ≥ p+1. Standard result; *cited from memory*.

---

## 3. Algorithms: what I can do below (a+1)(a+2)/2

I implemented the free-vector triangular solver for κ=2 with p ≡ 1 (mod 4) and verified every output.

**Free vector.** At quotient level ℓ, take ℓ+1 fresh columns and a dependency modulo F, the span of the earlier free vectors. Split the support into J₁ (square coefficients b²) and J₂ (coefficients ζb², ζ a fixed nonsquare). Then w₁ + ζw₂ ∈ F. Set u = w₂. For any c, c·u is represented exactly by J₂ when c is a square, or by J₁ up to an error in F when c is not (this uses that −1 is a square). The errors are cancelled top-down.

### (T1) Triangular plus base search — proved, experiment

**Method.** Stop the triangular recursion at quotient dimension ℓ₀. Solve the base by sampling the 2-dimensional kernel of ℓ₀+2 fresh projected columns.

- **Columns:** M = (a+1)(a+2)/2 − ℓ₀(ℓ₀+1)/2 + O(1).
- **Time:** 2^{ℓ₀+O(1)}·poly.
- **Correctness:** by the Weil bound, if the ℓ₀+2 linear forms are pairwise non-proportional (true for random columns), the projective kernel line has p/2^{ℓ₀+2} + O(ℓ₀√p) good points. This needs p ≫ 4^{ℓ₀}ℓ₀².

**Experiment (a = 30, p = 2^62+O(1), 5 runs each).**

| ℓ₀ | M | mean samples |
|---|---|---|
| 0 | 497 | 0 |
| 4 | 487 | 69 |
| 8 | 461 | 1350 |
| 12 | 419 | 27034 |

Saving Δ columns costs about 2^{√(2Δ)}. At M = εa² the time is 2^{a√(1−2ε)}.

### (T2) Lending — new; heuristic plus experiment

**Method.** For the first r levels, return the larger half of each dependency support to the column pool for later levels. In exchange, that level's cancelling coefficient must land in one prescribed square class: one bit per lender.

- A lent half is dependent modulo F because of its own level's relation. Later levels must therefore take one extra column per fully reused group and use a random kernel combination. Without this the next level only finds the trivial relation; that was a bug in my first version.
- The base is two fresh columns, retried until all r character constraints hold.

**Size.** M ≈ (a+1)(a+2)/2 − r(2a−r)/4. The expected time is 2^r·poly, *assuming* the r lender characters behave like independent fair bits (heuristic).

**Experiment (a = 30).**

| r | M | mean tries | 2^r |
|---|---|---|---|
| 0 | 497 | 1 | 1 |
| 4 | 426–437 | 16 | 16 |
| 8 | 366–378 | 179 | 256 |
| 10 | 344–359 | 1828 | 1024 |

**Consequences.**
- At M = εa² with ε ∈ [1/4, 1/2], the time is 2^{(1−√(4ε−1))a}. Near the top, M = (1/2−δ)a² costs 2^{≈2δa}, against 2^{a√(2δ)} for T1.
- In polynomial time (r = O(log a)): **M = (a+1)(a+2)/2 − Θ(a log a)**. This is a lower-order gain only.
- The residual work is exactly an r-shift power-residue pattern problem on the 2-dimensional base (§4.2). A 2^{o(r)}-time pattern solver would push T2's polynomial-time point to a²/2 − ω(a log a), but still not to o(a²).

### Why no c < 1/2 in polynomial time — argued

A free vector (one for which every multiple c·u is a P-combination) needs a nontrivial kernel of Λ_S. In a generic quotient of dimension ℓ that means |S| ≥ ℓ+1.

At large p, random columns are in general position in the relevant quotients. Then the sparse dependencies that KOW Lemma 2.3 exploits over F_3 do not exist. Supports must be disjoint because P is not closed under addition.

Every free-vector, flag or contraction design therefore pays about Σ(ℓ+1), apart from the per-level character bits that T2 trades for time.

---

## 4. Hardness direction

### 4.1 Direct sums do not amplify — proved

Since 0 ∈ P, a block-diagonal instance is solved by solving any one block. Hardness at large kernel dimension cannot come from independent copies.

### 4.2 Exact equivalence at M = a+2 — proved

**Reduction from the pattern problem.** Given N shifts c_i and target characters ε_i ∈ μ_κ, pick γ_i with χ(γ_i) = ε_i^{-1}. Build Λ with a = N−1 rows and M = N+1 columns, whose kernel is spanned by u = (γ, 0) and w = (γ∘c, 1).

- A solution with z₂ ≠ 0 gives K = z₁/z₂ satisfying χ(K + c_i) = ε_i, except possibly at one shift where K = −c_i.
- A solution with z₂ = 0 requires all ε_i to be equal.

**Converse.** A uniformly random instance with a 2-dimensional kernel is, after normalizing the basis, the same problem for uniform shifts and characters, up to one global twist.

So **random instances at M = a+2 are equivalent to "find K ∈ F_p with prescribed κ-th-power characters at ~a random shifts"**. That is Legendre or power-residue PRF key-finding from about a random (non-chosen) queries.

The only algorithm I know is roughly κ^a search. The cryptanalysis literature on the Legendre PRF (Khovratovich; Beullens et al.; Kaluđerović–Kleinjung–Kostić) needs many queries: *not checked*. This is conditional hardness, and only far below κa+1.

### 4.3 Planting obstruction — proved

**Lemma.** Let Λ have full rank a and M ≥ κa+1. Let T ⊆ [M] be such that every nonzero solution has x_T ≠ 0. Then the projection of K onto the coordinates in T has dimension at least (1 − 1/κ)|T| + 1/κ.

**Proof.** Let r′ be the rank of the columns outside T. If no solution vanishes on T, then by Chevalley–Warning on those columns M − |T| ≤ κr′. The projection of K onto T has dimension |T| − a + r′ ≥ |T| − a + (M − |T|)/κ. Substitute M ≥ κa+1.

**Corollary.** Any reduction that decodes from a block whose solution space projects to at most d dimensions needs |T| ≤ (κd − 1)/(κ − 1). For the 2-dimensional pattern problem that means at most 3 shifts. So §4.2's hardness cannot be planted inside an instance with M ≥ κa+1. Any hardness proof in the Chevalley–Warning regime must be non-local.

### 4.4 No reduction from MQ or SIVP — argued

- **MQ.** Writing general quadratics as sums of squares of linear forms needs *linear* constraints on s. The diagonal problem only permits linear constraints on s². Its solution set is φ⁻¹(U) with U = span(s²), of dimension dim U, and cannot cut out a dimension-n linear space.
- **SIVP (h ∈ {1,2}) and F_3 subset sum.** These live at κ = (p−1)/h or at p = 3. I know of no map between different primes.
- **Totality.** At M ≥ κa+1 the problem is total (Chevalley–Warning), so NP-hardness is excluded unless NP = coNP.
- **PPA_p.** The PPA_p-completeness of Chevalley–Warning (Göös–Kamath–Sotiraki–Zampetakis, *not checked*) is for fixed p and general polynomials. It does not cover diagonal forms with growing p.

---

## 5. The suggested routes

- **Regev/CLZ quantum decoding (the method behind KMOSW's εn²)** — proved obstruction, argued conclusion.
  - Take any product amplitude f supported on P.
  - By Tao's theorem, the LWE error support has size at least p + 1 − |P| ≥ (1 − 1/κ)p.
  - By Cauchy–Schwarz, every error value has probability at most |P|/p ≈ 1/κ.
  - Decoding would be random-linear-code decoding over F_p at error rate about 1 − 1/κ. Arora–Ge-style linearization would need degree about (1 − 1/κ)p, and no polynomial-time decoder is known at any m = poly(n).
  - Check: at p = 3, κ = 2 the bound gives support ≥ 2, i.e. binary errors, which is exactly KMOSW's case.
- **KOW CIS and halving machinery (Corollary 3.15)** — proved obstruction.
  - It needs an arithmetic progression of length 1 + 2⌊p/2k⌋ inside P.
  - An AP {x + iy} inside cH ∪ {0} gives a character sum over an interval of size at least t − 1. Pólya–Vinogradov then gives t ≤ √p log p + 1.
  - So k ≳ √p/(2 log p) and m ≳ (n²/2)^{k/2}, which is superpolynomial.
- **Lattices, Kirchner–Fouque/BKW, DEP, BGLS** — argued.
  - These target short coefficient vectors. Membership in P ignores size: κ-th-power residues are equidistributed in intervals much longer than √p log p.
  - Restricting to {0, ±1} ⊆ P gives SIS∞ with β = 1. That needs M ≳ a log p just for existence, and sits in KOW's Ω(n²) regime.
  - BKW-style trees with H-scaling, killing b coordinates per group by κ^b search, give time κ^{Θ(a/c)} at M = a^c.
- **Norm map (κ=2) and Weil descent** — argued.
  - Every element of F_p is a norm from F_{p²}. The norm relaxation is the instance with proportional column pairs (λ, −dλ), which is trivial and cannot be enforced on given columns.
  - Weil descent needs a non-prime base field.
- **Gröbner bases** — experiment. msolve over p = 65521; the problem is sliced to dimension 0 by a random linear subspace s = G(1, t). Each row below averages 2–3 trials.

| κ | a | M | degree (diagonal = dense) | msolve time, diagonal / dense | F_p points per slice |
|---|---|---|---|---|---|
| 2 | 9 | 19 | 512 | 0.28 s / 0.26 s | 0–3 |
| 2 | 10 | 21 | 1024 | 1.68 s / 1.67 s | 0–2 |
| 2 | 11 | 23 | 2048 | 11.2 s / 11.3 s | 0–2 |
| 3 | 6 | 19 | 729 | 0.22 s / 0.22 s | 0–3 |

  - For every a from 2 to 11 (κ=2, M = 2a+1 and 3a) and every a from 2 to 6 (κ=3, M = 3a+1), the degree is exactly κ^a and diagonal and dense systems take the same time.
  - Time grows about 6.5× per unit of a, roughly degree^{2.7}.
  - The diagonal structure gives Gröbner bases no advantage. Structure-preserving slices (setting s_i = c·s_j) are just contraction steps.

---

## 6. Precise open question

For fixed κ ≥ 2, is there a classical or quantum algorithm running in time poly(a, log p) that does the following, for all large primes p ≡ 1 (mod κ):

- input: uniformly random λ_1..λ_M ∈ F_p^a, with
  - (A) M = c·a² for some constant c < 1/2, or
  - (B) M = o(a²);
- output: x ∈ P^M with x ≠ 0 and Σ x_i λ_i = 0, with probability at least 1/poly?

Known so far:
- T2 gives a²/2 − Θ(a log a) in polynomial time, and (1/2 − δ)a² in time 2^{O(δa)}.
- Question (A) is the large-p analog of KOW's n²/3 for F_3. It needs dependencies cheaper than ℓ+1 columns per level.
- Any route through Regev's reduction must decode at error rate 1 − 1/κ (§5).
- Any hardness proof at M ≥ κa+1 must avoid planted low-dimensional cores (Lemma 4.3).

**Concrete next test.** Can the r-bit lender constraints in T2 be solved in 2^{o(r)} time? They form an r-shift power-residue pattern problem on a 2-dimensional base. A yes would not reach o(a²), but would show the pattern problem is the bottleneck.

**Sources:** [Ivanyos–Santha](https://arxiv.org/abs/1503.09016) · [Kothari–O'Donnell–Wu](https://arxiv.org/abs/2510.07515) · [Kothari–Metger–O'Donnell–Shutty–Wu](https://arxiv.org/abs/2609.40321) · [Huang–Bao](https://arxiv.org/pdf/1507.03674) · [Thomae–Wolf](https://link.springer.com/content/pdf/10.1007/978-3-642-30057-8_10.pdf) · [Hashimoto 2021/1045](https://eprint.iacr.org/2021/1045) · [ePrint 2026/1054](https://eprint.iacr.org/2026/1054) · [Kirchner–Fouque](https://arxiv.org/abs/1506.02717) · [Ducas–Espitau–Postlethwaite](https://eprint.iacr.org/2023/1125) · [Bai–Galbraith–Li–Sheffield](https://eprint.iacr.org/2014/593)
