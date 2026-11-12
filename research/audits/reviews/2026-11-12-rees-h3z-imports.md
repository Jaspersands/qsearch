# Import checks for Theorem A of `2026-11-12-rees-h3z-infinite-index.md` (2026-11-12)

**Status: AI-checked, pending human review.** One Claude Code helper pass. I acted as a hostile
human referee on the three imports that `2026-11-12-rees-h3z-referee.md` left open. No existing
file was edited, no Git command was run, and the claim gates are unchanged
(`speedup_claim_allowed` and `novelty_established` stay false).

Sources:
* Kuperberg, arXiv:2507.18499v1. I used the local pdftotext file `2026-11-12-rees-h3z-referee/k.txt`,
  split into columns by `2026-11-12-rees-h3z-imports/split.py` into
  `2026-11-12-rees-h3z-imports/sources/kuperberg_columns.txt`. Page numbers below are PDF pages,
  which match the printed numbers. I read §1 (Thms 1.5, 1.8), §2.4 and all of §7 (pp. 19–36).
* Ivanyos–Sanselme–Santha, arXiv:0707.1260**v1** (9 Jul 2007, the only arXiv version). The PDF was
  fetched from arxiv.org and its text is in `sources/iss.txt`. The Algorithmica 2012 version is not
  on arXiv and was not read.
* Imran–Ivanyos, arXiv:2304.08376**v1** (17 Apr 2023, the only version). The text is in
  `sources/ii.txt`; I read §§1–3 and the statements in §§4–6. The QIP 2024 version was not read.

All files under `sources/` are untrusted extracted data.

Falsification check: `cf_check.py` (output in `cf_check.out`, run with
`nice -n 19 /opt/anaconda3/bin/python -I cf_check.py 7`). It checks the step-5 continued-fraction
cutoff when only an upper bound n' is known (20,000 random cases, 0 failures) and the box
arithmetic of Step 2. It proves nothing beyond the instances tested.

## Verdict summary

| # | Question | Verdict |
|---|---|---|
| 1a | Worst-case or expected time | **CONFIRMED: worst case.** Bounded error, with fixed step counts. |
| 1b | Must n be given; is an upper bound n' ≥ n enough | **CONFIRMED.** n, or a bound on it, must be supplied, and any n' ≥ n works. |
| 1c | What "good probability" means; amplification | **CONFIRMED: a constant.** It is not stated; I assemble it as ≥ 1/2 − O(S^-2) for steps 1–6, times Shor–Kitaev's constant. Amplification works, **with a new box fix (G1)**. |
| 1d | Query range | **WRONG in the note.** Step 7 also queries f∘A_6, outside the cube, at a range the paper never states. Fix F1. |
| 1e | Is the proof of Thm 7.1 complete | **Mostly.** It is a full proof, not an outline, with standard facts left unproved. **Gap: the full-rank case ℓ = k is excluded "for convenience" in §7.7.** That case is exactly rk π(H) = 2 in Theorem A. Fix F2. Line-by-line check of Lemmas 7.6 and 7.16: **STILL NEEDS HUMAN**. |
| 1f | Hidden assumptions on f; restricting to the cube | **CONFIRMED harmless for steps 1–3.** Steps 7, the membership checks and failed runs need F1 and G1. |
| 2a | ISS 2012 for UT_3(Z/q^k), q ≥ 3 | **CONFIRMED** against arXiv v1, with input-model caveats (F3). Journal numbering: STILL NEEDS HUMAN. |
| 2b | Imran–Ivanyos Thm 1 at q = 2 | **CONFIRMED** against arXiv v1, with the purification oracle of cor:nilpotent. |
| 2c | The note says Step 3 rk 2 uses "cor:utz … and not Thm is-import" | **WRONG.** cor:utz as stated assumes is-import, and so does its proof for n = 3. The note uses a variant. Fix F3. |
| 3 | Step 2 parameters (box 2P_K + 3b + 3, n_L = O(b)) | n_L = O(b) and the box arithmetic are **CONFIRMED**. P_K must also cover step 7 and the checks (F1, G1). P_K is in fact **linear** in n_L for k = 3, but the constant is never computed in the paper. |

## 1. Kuperberg 2025

### (a) Worst-case or expected time. CONFIRMED: worst case, bounded error.

*Locator:* Thm 1.5 (p. 2); Algorithm A, §7.1 (pp. 19–20); Thm 7.1 (p. 20); the end of §7.8 (p. 36).

Theorem 7.1 says that, with suitable Q, R, S, T, Algorithm A "runs in BQP and succeeds with good
probability". §7.8 (p. 36) gives the cost of each step:
* steps 1–3 are quantum polynomial;
* steps 4–6 are classical (LLL, continued fractions, Kannan–Bachem SNF), each in P;
* step 7 is Shor–Kitaev.

No step is a loop that repeats until success. My check of the failure branches: when the sample is
bad, step 4 still runs LLL on a fixed-size rational basis, whose denominators divide lcm(T,Q)
(p. 33). Step 5's B_2 exists and has |det B_2| ≥ t and ‖B_2^{-1}‖ ≤ T for every outcome, because
Lemma 7.20's proof (p. 34) uses only ‖b_j‖ ≤ r < 1. So the cost is a worst-case bound for every
outcome, and the algorithm is Monte Carlo (bounded error, not Las Vegas). The approximate
Gaussian-state preparation (Grover–Rudolph / Kitaev–Webb, step 1) has no explicit error budget. It
is standard and costs poly time for exponentially small error, but it is not written out.

### (b) Must n be given? Does an upper bound n' ≥ n work? CONFIRMED (PROVED given Kuperberg's lemmas).

*Locator:* the start of §7.8 (p. 33) says that every parameter depends only on n = ‖M‖_bit of the
output. The constraint list and the choices R = 2^{Θ(n)}, …, Q = S² are on p. 36, and (7.38)–(7.50)
are on pp. 34–36.

So n, or a bound on it, must be supplied; Thm 1.5's statement hides this. Every constraint in the
p. 36 list is a lower bound on R, R_1, T, S or Q in terms of k, an absolute constant C, and
Δ < 2^{2n}:
* Δ < 2^{2n} is (7.38);
* R ≥ 2^{2n+1} is (7.39);
* R_1 ≥ max(Δ, 2^k, C) and R_1 ≥ 2^{k+1}R;
* Λ = R_1^{Ck};
* T ≥ ΛR_1;
* S ≥ max(Δ², C, Λ√k, T√k, 2T², 4R²T³);
* Q ≥ S².

Each still holds if n is replaced by n' ≥ n. Lemma 7.16 holds for any integer R_1 above its bound.

The only place where R acts as a cutoff, not a lower bound, is the denominator cutoff in step 5.
There the true denominators divide |det M_1| < 2^n (p. 36), and the noise per entry is below
4sT³ ≤ R^{-2} by (7.50). Kuperberg only says "denominators bounded by R". I fill in that the
output is the **last convergent with denominator ≤ R**. Legendre makes a/b a convergent, since
R^{-2} < 1/(2b²). The next convergent p'/q' satisfies 1/R² > |x − a/b| > 1/(b(b+q')), so
q' > R²/b − b > R, because b < 2^n ≤ √(R/2). This holds for any R ≥ 2^{2n'+1}, n' ≥ n.
`cf_check.py` found 0 failures in 20,000 random cases with n' − n ∈ [0,6].

So running Algorithm A with n' ≥ n is correct, in time poly(k, n').

### (c) What "good probability" means, and amplification. CONFIRMED: a constant. Amplification is sound after G1.

*Locator:* Lemma 7.6 (p. 25; probability ≥ 3/4, proved on p. 30 via (7.23), 1/(2π) + O(s));
Lemma 7.16 (p. 30; ≥ 3/4); Lemma 7.21 (p. 35; ≥ 3/4, the same event as Lemma 7.6); (7.43)
(p. 34; the same event); step 7 (p. 36, "Shor–Kitaev"); §7.3 (p. 21; O(log|H^#|) samples generate
H^# "with good probability").

The paper never combines these. My assembly, labelled PROVED given the lemmas:
* Steps 1–6 succeed whenever both the Lemma 7.6 event and the Lemma 7.16 event hold. So their
  success probability is ≥ 1 − 1/4 − 1/4 − O(s²) = 1/2 − O(S^{-2}). Lemma 7.16's probability is over
  a uniform y_0 ∈ H^# with y_1 adversarial within 1/Λ, and Lemma 7.6 couples y_1 = y_0 + u with
  y_0 uniform, so the union bound applies.
* Step 7 multiplies this by the standard constant success probability of Shor–Kitaev.

So "good probability" means a positive absolute constant, not 1/poly.

Amplification by membership checks is sound. Every vector v that passes F̃(v) = F̃(0) lies in L.
The union over runs generates a sublattice of L, and it equals L as soon as one run outputs a
basis of L. O(log 1/ε) runs then give error ≤ ε/4. **G1 (new gap):** the check F̃(v) = F̃(0) is
meaningful only if the query for v lies in the coherent box. A failed run can output a vector with
huge entries, the oracle is unspecified there, and a wrong vector could then pass. Fix: LLL-reduce
each run's output basis, discard any vector with ‖v‖_∞ ≥ 2^{4b+5}, and only then test. A correct
run's reduced basis passes: by Thm 7.19 (p. 33) applied to the basis of L with entries
< 2^{4b+2}, its vectors have norm < 2^{4b+5}. The resulting queries have matrix entries
< e·2^{8b+10} + 2^{4b+5} < 2^{11b+12} ≤ 2^{20b+11}.

### (d) Which points are queried. The note is WRONG (step 7 omitted). Fix F1.

*Locator:* step 2 (p. 19) applies U_f restricted to the cube ‖x‖_∞ < Q/2 (one query, in
superposition). Step 7 (p. 20) finds A_6^{-1}(H) as the hidden subgroup of x ↦ f(A_6 x) by
Shor–Kitaev.

Step 7 queries the points A_6 x for x in the Shor–Kitaev range on Z^ℓ. The paper specifies neither
that range nor a bound on the entries of A_6 = V^{-1}[I_ℓ; 0], where V comes from Kannan–Bachem's
SNF of A_5. A bound exp(poly(n)) follows from Kannan–Bachem's polynomial output size, because A_5
has denominators ≤ R and entries ≤ T + 1. That makes step 7's range exp(poly(n)), but this is
implicit. The note's sentence "Algorithm A applies the hiding function only on the cube" is
therefore false.

**F1:** before step 7, replace A_6 by an LLL-reduced basis A_6' of H_1. Then ‖columns‖ ≤
2^{ℓ−1}·2^n, by Thm 7.19 with the columns of M ⊆ H ⊆ H_1. Run Shor–Kitaev with index bound
[H_1:H] = √(Δ/Δ_1) ≤ 2^n ((7.24), p. 30) on a cube of side 2^{2n+O(1)}. Its queries then have
entries 2^{3n+O(k)}. Since A_6' is known classically before step 7, abort the run, with no query,
if its range exceeds the box. This keeps failed runs inside the oracle's domain. (F1 is argued
here; the standard Shor–Kitaev box was not re-derived. Mosca–Ekert is still unread.)

Size of the step-2 cube, from p. 36 with k = 3. Take R = 2^{2n+1}, R_1 = 2^{k+1}R (≥ C),
Λ = R_1^{Ck}, T = ΛR_1, S = 4R²T³ and Q = S². Then log_2 Q = (36C + 20)n + 90C + 38, where C is
Lemma 7.16's absolute constant. (Kuperberg writes R_1 = 2^{Θ(nk)} and Q = 2^{Θ(nk²)}. These are
valid upper bounds, but R_1 = 2^{Θ(n+k)}.) **C is never computed.** The contradiction at the end of
Lemma 7.16 (p. 33) is Λ_1 ≤ 16R_1^{12k−4ℓ+1/2} + exp(−Ω(R_1^4)), which suggests C_1 = 13 and C = 14
suffice, but I have not verified this, and the exp(−Ω(·)) terms in Lemmas 7.6, 7.7 and 7.11 carry
further implicit thresholds. So P_K = O(n_L) = O(b) only up to an unknown absolute constant. As an
existence statement, B = poly(b) (indeed O(b)) is fine. An implementation would first have to
extract C.

### (e) Is the proof of Thm 7.1 complete? Mostly. Gap F2 (ℓ = k). Analytic core: STILL NEEDS HUMAN.

*Locator:* the omission sentence ("We omit some of the statistical estimates", p. 3) belongs to
**Thm 1.8 and §8**. §7 is not labelled as an outline, and Thm 7.1 is said to be proved in
§§7.4–7.8 (p. 20). Inside §7:
* Propositions 7.3, 7.4 and 7.5 (pp. 24–25) and Lemma 7.8 (p. 26) are stated without proof as
  standard facts.
* (7.19) is proved "skipping some details" (p. 28).
* There are typos: "k+1−ℓ vanishing rows" in step 6 should be k − ℓ; y_2 is used for y_0 in (7.32);
  and the "+2" on p. 32.
* The combined probability is never assembled (see (c)), and the step-7 parameters are never given
  (see (d)).

None of these looks fatal.

**F2 (material for Theorem A).** §7.7 (p. 30) assumes ℓ < k "for convenience", since ℓ = k is
Shor–Kitaev. Lemma 7.16 is the only source of the k + 1 − ℓ short LLL vectors, so step 4's rank
detection is not proved for ℓ = k. In Theorem A, L ⊆ Z^3 has rank 3 exactly when rk π(H) = 2. A
misdetection there sends the run into Step 3's rank-1 branch, which outputs a proper subgroup of H
and cannot detect the error.

Two fixes:
* **(i) Argued fill.** For ℓ = k, H^# is finite, and λ = ord(y_0) ≤ |H^#| = √Δ < 2^n gives the
  lattice vector (λu, λt), of norm ≤ 2^n(√k·s + t) ≪ 2^{-k}r. Every LLL vector of norm ≤ r lies in
  span(H_R^⊥ ⊕ 0, (u, t)), which has dimension k + 1 − ℓ = 1 here. (This also gives the upper bound
  k + 1 − ℓ on the count for every ℓ.) So step 4 returns ℓ = k.
* **(ii) Robust fix, recommended.** In Step 2, also run standard finite-index Shor–Kitaev on F̃
  over Z^3, with index bound 2^{4b+2} and cube side 2^{8b+5}, and add its verified vectors to the
  pool. It is correct whenever L has full rank, and harmless otherwise. Its matrix entries are
  < 2^{19b+12} ≤ 2^{20b+11}.

The analytic core is Lemma 7.6 (Fourier stage, pp. 25–30) and Lemma 7.16 (the Weyl-type dense-orbit
bound, pp. 30–33). I read both and found no error in the steps, but I did not verify every
estimate line by line. That needs a human.

### (f) Hidden assumptions on f; restricting to the cube. CONFIRMED harmless for steps 1–3. Steps 7, checks and failures need F1/G1.

*Locator:* §2.4 (p. 6): f is a subroutine or oracle whose cost is polynomial in the input length,
and the running time is parametrized by the calls needed to witness generators of H. Lemma 7.9
(p. 27) compares with the ideal state U_f|ψ_G⟩ on all of Z^k. (7.12) (p. 27) measures the output
register only to simplify the analysis.

The all-Z^k objects are proof devices. They need f to be a genuine hiding function on Z^k, which
F̃ is, since f hides H on all of G, but they are never queried. The algorithm itself queries only
the cube (step 2) and step 7's range. The analysis uses only ‖U_f‖_{1→1} = 1 and discrete labels X
(the mixed norm ‖·‖_{∞,1} sums over labels a ∈ X, p. 26). So the polynomial-cost assumption is used
only on the points actually queried, and our box oracle satisfies it there.

Side remark, outside Theorem A: Lemma 7.9's argument sums over a discrete label set X. That
supports keeping Theorem B1 CONDITIONAL on I1 (state-valued labels).

## 2. cor:utz at n = 3

Core: `docs/papers/rees-hsp/core/main-core.tex` lines 811–834 (cor:utz) and 782–809 (cor:nilpotent).

### (a) ISS 2012 for UT_3(Z/q^k), q ≥ 3. CONFIRMED against arXiv v1, with caveats.

*Locator (arXiv v1):*
* Thm 1 (p. 2): any nil-2 group with an oracle f hiding H; an efficient quantum procedure finds H.
* §2.1 (p. 3): hiding sets on left cosets.
* §3 (p. 5): elements are normal words of a refined polycyclic presentation with a polynomial-time
  collection procedure. A black-box solvable group is converted by the quantum Beals–Babai of
  Ivanyos–Magniez–Santha.
* Thm 2 and Lemmas 1–3 (pp. 5–6): the Sylow split, the reduction to |H| ≤ p, and the reduction to
  exponent p when p exceeds the class.
* Thms 3–5 (pp. 7–9).
* p. 11: the only randomness is choosing a quadratic non-residue.
* Efficiency means polylogarithmic in |G| (p. 2).

Fit with cor:utz's quotient:
* UT_3(Z/q^k) is nil-2 and q > 2 = class, so Lemma 3's main path applies.
* An explicit refined polycyclic presentation is available. Use x^a y^b z^c with base-q digits of
  a, b, c in [0, q^k). Collection is matrix multiplication mod q^k, so Beals–Babai is not even
  needed.
* The oracle is the standard U_f: Lemma 4 creates Σ_g|g⟩|f(g)⟩.
* Cosets are left cosets, matching f(x) = f(y) ⟺ x^{-1}y ∈ H.
* The output is generators of H.
* log|G| = O(b) here.

Caveats:
* Thm 1 states neither an error bound nor a formal input model. Both are implicit: bounded error,
  through Fact 1 (the standard abelian algorithm). Amplify by taking the union of the outputs that
  pass f(h) = f(1); the outputs are lifts in [0, M), inside the box.
* For q = 2, ISS v1 Lemma 3 (p. 6) defers to Friedl et al. (STOC 2003) in a single sentence. I
  could not check that this covers 2-groups of class 2 with large exponent. Imran–Ivanyos's own
  survey of related work (p. 4) says that Friedl et al. need bounded exponent, while it also says
  that ISS handles class 2 for all primes. So q = 2 in ISS: **STILL NEEDS HUMAN** (the journal
  version and Friedl et al.). Theorem A avoids this case by using Imran–Ivanyos at q = 2.
  rem:utz-scope(b) and rem:nilpotent-scope(b), which say ISS covers every prime at class two,
  inherit this caveat.
* The theorem numbering was checked in arXiv v1 only. The Algorithmica 2012 numbering is
  unchecked.

### (b) Imran–Ivanyos 2023 Thm 1 at q = 2. CONFIRMED against arXiv v1.

*Locator (arXiv v1):*
* Thm 1 (p. 4): nilpotent of bounded class; the prime factors of |G| bounded by a constant; a
  black-box group with unique ℓ-bit encoding; an exact algorithm using poly(ℓ) operations and
  poly(log|G|) calls to the subgroup-state oracle and its inverse.
* p. 3: the oracle returns, on zero input, a fixed purification of Ξ_{G,H} (left cosets).
* §2.2 (p. 6) and Prop 1 (p. 9): the prime factors are known or given.
* Lemma 1 (p. 8): the purification characterization.
* §2.1 (p. 5): exactness assumes exact QFTs modulo the primes, which take O(1) gates for bounded
  primes.

Fit: the Sylow 2-subgroup of UT_3(Z/M) is UT_3(Z/2^k) by CRT. It is a 2-group of class 2 with known
prime {2}. Matrices mod M give a unique encoding, and the group operations are matrix arithmetic.
The oracle and its inverse are the ones built in cor:nilpotent's proof (core lines 798–799): an
exact uniform superposition over the 2-part, then U_f, then the inverse. By Lemma 1 this is a
purification, because f restricted to the 2-part hides H ∩ G_2. That restriction is valid because
x^{-1}y stays in G_2 (cor:nilpotent (a)). Compiling to a finite gate set makes the step non-exact,
with error ≤ ε/4, as cor:nilpotent states. The QIP 2024 version is unchecked.

### (c) The note's attribution of Step 3 (rank 2). WRONG; fix F3.

cor:utz is stated with "assume Theorem is-import" (core line 819). Its proof goes cor:utz →
cor:nilpotent (c = 2) → cor:black-box-pe (Thm main plus is-import) at the odd primes, and
Imran–Ivanyos only at p ≤ 2 (core lines 796–798). So "Apply cor:utz … For n = 3 it uses ISS 2012
(q ≥ 3) … and not Thm is-import" mixes two routes. What Theorem A needs is the **variant** that
rem:utz-scope(b) sketches, made precise at q = 2:
* cor:utz's congruence-subgroup and period step;
* the CRT split of UT_3(Z/M);
* ISS Thm 1 at each odd q, and Imran–Ivanyos Thm 1 at q = 2.

## 3. Theorem A, Step 2 parameters, re-checked

| Claim in the note | Check | Verdict |
|---|---|---|
| n_L = O(b) | L has a basis with entries < 2^{4b+2} in every rank (referee's derivation, re-read). (7.38) needs only Δ ≤ 2^{2d}, with d the digits of any basis, so the HNF form is irrelevant. n' = 9(4b+3) + O(1) is computable from b. | CONFIRMED |
| Run Algorithm A "at that n_L" | An upper bound suffices (1b). | CONFIRMED |
| Queries have entries < 2^{P_K}, P_K = poly(n_L) | Step 2's cube: P_K = log_2 Q − 1 = (36C+20)n_L + O(C), linear with an uncomputed C. Step 7 is not covered by "the cube". | WRONG as worded; fix F1 |
| Matrix entries < e·2^{2P_K} + 2^{P_K} < 2^B with B ≥ 2P_K + 3b + 3 | (eα, β, γ + eαβ) with e < 2^{3b+1}: the maximum is < 2^{2P+3b+2} (`cf_check.py`). | CONFIRMED (one spare bit) |
| Repeat and keep v with F̃(v) = F̃(0) | Sound only for v inside the box. | GAP G1; fix by filtering |
| "good probability" is a constant (assumed) | ≥ (1/2 − O(S^{-2}))·p_SK. | CONFIRMED |
| Thm 7.1 with an upper bound on n (assumed) | | CONFIRMED |
| Rank 2 handled by Algorithm A | ℓ = k is excluded in §7.7. | GAP; fix F2 |

The new query ranges fit the existing box. Membership checks need exponent 11b+12 and the parallel
Shor–Kitaev 19b+12; both are ≤ 20b+11 for b ≥ 1. Step 7 after F1 queries vectors with entries
2^{3n_L+O(1)}, which is covered once P_K is defined as the maximum over steps 2 and 7. So
B = max(20b + 11, 2P_K + 3b + 3) stays valid, with P_K redefined as in the replacement text below.

## Replacement text for the note (not applied)

**F1 + G1, replacing the Kuperberg bullet under "Imported results":**
> * Kuperberg 2025, arXiv:2507.18499v1, Thm 1.5 via Thm 7.1 / Algorithm A (§7.1; proof §§7.4–7.8,
>   read 2026-11-12, `2026-11-12-rees-h3z-imports.md`). Algorithm A takes the answer size n, or
>   any upper bound n' ≥ n. All of its parameters are lower bounds in n (§7.8, p. 36), so
>   n' works, in time poly(k, n'). It runs in worst-case polynomial time, with constant success
>   probability (≥ 1/2 − o(1) for steps 1–6, by Lemmas 7.6 and 7.16, times Shor–Kitaev's constant
>   in step 7). It queries f on the cube ‖x‖_∞ < Q/2, with log_2 Q = O(k(n+k)) and an absolute
>   constant that the paper does not compute (step 2). It also queries f∘A_6 in step 7, whose range
>   is not stated. We LLL-reduce A_6 and skip any run whose step-7 range leaves the box. The proof
>   assumes rank ℓ < k in §7.7; the full-rank case is covered below by a parallel Shor–Kitaev run.
>   Lemmas 7.6 and 7.16 are read but not verified line by line (pending human review).

**F1 + F2 + G1, replacing the end of Step 2 from "Run Algorithm A at that n_L.":**
> Run Algorithm A with the bound n' = 9(4b+3) + O(1) ≥ n_L. Before step 7, replace A_6 by an
> LLL-reduced basis of H_1, and skip the run if step 7's query range leaves the box. In parallel,
> run finite-index Shor–Kitaev on F̃ over Z^3 with index bound 2^{4b+2} (cube side 2^{8b+5}); it
> returns L whenever rk π(H) = 2, i.e. rk L = 3, the case Kuperberg's §7.7 sets aside. Let 2^{P_K}
> bound the entries of every vector queried by these runs. Then P_K = O(n_L) = O(b), with an
> absolute constant from Kuperberg's Lemma 7.16 that is not computed, so we state P_K = poly(b).
> The matrix entries are < e·2^{2P_K} + 2^{P_K} < 2^B. Repeat O(log 1/ε) times. LLL-reduce each
> run's output, discard vectors with ‖v‖_∞ ≥ 2^{4b+5} (these queries stay below 2^{11b+12}), and
> keep the remaining v with F̃(v) = F̃(0). Every kept vector lies in L. Each run succeeds with
> constant probability, so the lattice the kept vectors generate is L with probability ≥ 1 − ε/4.

**F3, replacing the Step 3 rank-2 bullet's last two sentences:**
> Apply the reduction in the proof of cor:utz (periods of x, y, z; M = lcm; Γ(M) ⊆ H; the quotient
> UT_3(Z/M), queried on [0, 2^{20b+11})). Do not apply cor:nilpotent. Split UT_3(Z/M) by CRT into
> the groups UT_3(Z/q^k). For each odd q use ISS (arXiv:0707.1260v1, Thm 1, via its Lemmas 1–3
> and Thms 3–5), with the explicit polycyclic presentation by base-q digits, amplified by the union
> of outputs h with f(h) = f(1). For q = 2 use Imran–Ivanyos (arXiv:2304.08376v1, Thm 1), with the
> purification oracle of cor:nilpotent's proof. This route does not use Thm is-import. It is not
> cor:utz as stated, which assumes is-import. Error ε/2. ISS's own q = 2 case (its Lemma 3 cites
> Friedl et al.) is not used.

**Header of Theorem A:** replace "and cor:utz" with "and the n = 3 route of cor:utz (ISS 2012 Thm 1
at odd q, Imran–Ivanyos 2023 Thm 1 at q = 2; arXiv versions checked)".

## Still needs a human

1. Line-by-line verification of Kuperberg's Lemmas 7.6 and 7.16 (§§7.6–7.7), and a value for the
   absolute constant C if an explicit B is wanted.
2. The step-7 Shor–Kitaev parameters and box (F1), and Mosca–Ekert §§2, 4.2, still unread.
3. ISS at q = 2 (Lemma 3 → Friedl et al.) and the Algorithmica 2012 and QIP 2024 theorem numbers.
   Theorem A does not depend on this point after F3, but rem:utz-scope(b) and
   rem:nilpotent-scope(b) do.

## Adversarial self-check

* **Could step 2's cube already be the whole query range?** No. Step 7 is a separate Shor–Kitaev
  call on f∘A_6 (p. 20). Since the multi-sample variant that absorbs step 7 (§7.2) is only
  heuristic, step 7 is needed.
* **Is ℓ = k really excluded?** Yes: p. 30 assumes ℓ < k for convenience. My fill (i) is argued,
  not checked against Kuperberg's text, which is why (ii) is the recommended fix.
* **Is the union-bound constant right?** Lemma 7.16 holds with y_1 adversarial within 1/Λ. If the
  coupling in Lemma 7.6 did not make y_0 marginally uniform, the bound would fail. The proof gives
  (7.20), a Gaussian around a uniform H^# point up to exp(−Ω(S)), so I accept it, but this is
  where a human should look.
* **Does an upper bound n' break Lemma 7.16's choice Λ = R_1^{Ck}?** No. The lemma holds for any
  integer R_1 ≥ max(Δ, 2^k, C).
* **Did I overstate the ISS fit?** Thm 1 in v1 is informal. The fit relies on §3's
  polycyclic-presentation model and on Fact 1's bounded error. A referee could ask for the journal
  version's precise statement.
* **Did I verify the Imran–Ivanyos inverse-oracle construction?** Only by reading cor:nilpotent's
  text against Lemma 1. Its exact-Watrous preparation (II22) was not read.
* **Finite checks** (`cf_check.py`) can only falsify. 0 failures proves nothing.
