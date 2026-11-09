# Type certificate: proof check, low-support classes, thresholds

AI-only report (2026-11-09), pending human review. Written by a subagent and saved by the parent.
The parent re-derived the permanent identity P(a(e_j−e_j′)) = −κ(κ−2)! and reran
`../types/sep_types.py 4 137 181 193 197 229`, which reproduced PW = 1.652, 0.9056, 1.0131, 0.8271,
0.6125. Context: `../../2026-11-09-rees-square-gap-stepanov.md` §3. Runs used
`nice -n 19 /opt/anaconda3/bin/python -I`, κ ≤ 4. Labels:
- [proved]
- [proved mod Weil]: everything except the cited Weil bound for complete character sums on P¹
- [computed]: exact finite computation by the script named
- [argued]: has a named non-rigorous step
- [heuristic]

## 1. Dictionary [proved]

Notation: χ(x) = ω^{ind x}, χ(0) = 0, n = p+1−2κ, h = (p−1)/κ. Configurations are (S,T,z), 2κ+1
labelled distinct points of P¹. A chart is g with g(z) = ∞, α_j = g(s_j), β_i = −g(t_i).

- Affine orbits of (α,β) correspond to PGL₂-orbits of (S,T,z). Both actions are free.
- The pattern mod constants is P_ij ≡ ind(t_i−s_j) − ind(s_j−z) − ind(t_i−z). To see it, take
  g = 1/(x−z), so g(s)−g(t) = (t−s)/((s−z)(t−z)).
- (C1), meaning ind(t_i−s_j) = a_i+b_j, depends only on (S,T).
- F(U,V) = N(U⊕V)/(p·h). So F counts PGL₂-orbits of (C1) configurations with type (U,V), with
  types taken mod a constant on EACH side.
- F(−ι,−ι)·p·h is the number of all-nonzero contractions.
- Changing the generator ξ = g^u turns the pattern into −u(i+j), which is still a bijective type.

## 2. Validity of the permanent-weighted certificate [proved; computed]

**Theorem 1.**
- (i) F(U∘σ+a, V∘τ+b) = F(U,V).
- (ii) F̂(r,c) = 0 unless Σr ≡ Σc ≡ 0.
- (iii) κ^{2κ}(κ!)² F(−ι,−ι) = Σ_ρ F̂(ρ)P(r)P(c), with P(r) = Σ_σ ω^{−Σ r_iσ(i)}.
- (iv) If PW < 1, then F(−ι,−ι) ≥ κ^{−2κ}F̂(0)(1−PW) > 0, so p ∉ E₂′(κ) ⊇ E₂(κ).

*Proof.*
- (i): relabel rows and columns; the shifts are already summed in F.
- (iii): average Fourier inversion over the S_κ×S_κ orbit of the bijective types, on which F
  is constant.
- (iv): P(0) = κ!.

**[computed]** `cert_check.py`:
- the identity holds to ≤ 4·10⁻¹¹ relative error at κ = 3 (p = 19..223) and κ = 4 (p = 61..509);
- F is exactly invariant under the permutations checked.

κ = 4 values of PW / PW_pair (cert_k4.out, cert_k4_low.out):

| p | PW | PW_pair |
|---|---|---|
| 61 | 12.0 | 6.05 |
| 73 | 7.58 | 4.00 |
| 89 | 4.21 | 2.30 |
| 97 | 4.00 | 2.26 |
| 101 | 3.00 | 1.70 |
| 109 | 2.59 | 1.49 |
| 113 | 2.87 | 1.68 |
| 137 | 1.65 | 0.940 |
| 149 | 1.29 | 0.731 |
| 157 | 1.12 | 0.620 |
| 173 | 1.11 | 0.651 |
| 181 | 0.906 | 0.514 |
| 193 | 1.013 | 0.604 |
| 197 | 0.827 | 0.477 |
| 229 | 0.613 | 0.336 |
| 349 | 0.319 | 0.162 |
| 509 | 0.195 | 0.093 |

- Correction to the parent note: PW first certifies at p = 181, not 197.
- At κ = 3, PW first certifies at 43 and PW_pair at 31.

## 3. Pair-signed certificate [proved]

- 𝓟 = pair one-sided frequencies: c = a(e_j−e_j′) with r = 0, or the transpose.
- Their permanent weights are P(a(e_j−e_j′)) = −κ(κ−2)!, so S_pair = −κ!·κ(κ−1)/2.
- Main terms −κF̂(0)/n move to the main side:
  - D = 1 + κ²(κ−1)/n;
  - N = [Σ_𝓟 |F̂+κF̂(0)/n||PP| + Σ_rest |F̂||PP|]/(F̂(0)(κ!)²);
  - κ^{2κ}F(−ι,−ι)/F̂(0) ≥ D − N.
- PW_pair := N/D < 1 certifies.
- [computed] Checked at (3,19), (3,31), (3,37), (4,89).
- Signing all one-sided classes instead is valid but worse.

## 4. Low-support classes

**Theorem 3 [proved].** Take r = 0, c ≠ 0, Σc ≡ 0, G_c(x) = Π χ^{c_j}(x−s_j) and
Λ_c(S) = Σ_{x∈P¹∖supp} G_c. Then n·F̂(0,c)/F̂(0) = −κ + E_(C1)[conj G_c(t₀)(Λ_c(S) − Σ_{l∉supp} G_c(s_l))].
The −κ comes from the points z ∈ T, where (C1) makes G_c constant.

**Corollary 3.1 [proved] (pair classes).** For c = a(e_j−e_j′), x ↦ (x−s_j)/(x−s_j′) is a bijection
of P¹∖{s_j,s_j′} onto F_p^×, so Λ = 0. Hence:
- n·F̂/F̂(0) = −κ − R with |R| ≤ κ−2;
- 2/n ≤ |F̂|/F̂(0) ≤ (2κ−2)/n, and Re ≤ −2/n.

[computed] Class means of n·F̂/F̂0:

| (κ,p) | (3,19) | (3,31) | (3,151) | (4,193) | (4,197) | (4,349) | (4,509) |
|---|---|---|---|---|---|---|---|
| mean | −2.500 | −2.857 | −2.974 | −4.023 | −3.816 | −3.900 | −3.934 |

**Theorem 4 [proved mod Weil].** For every ρ ≠ 0 with total support m:
- |F̂(ρ)|/F̂(0) ≤ ((m−2)√p + 2κ−m)/n.
- The bound is sharp: it is attained at (3,19).
- Observed ratios to the bound are ≤ 0.74 (κ = 3, p ≥ 31) and ≤ 0.69 (κ = 4).

**Other classes.**
- One-sided classes with support ≥ 3 are O(1)/n with no −κ [computed]. A Poisson-bucket
  explanation is [heuristic].
- (2,2) classes are O(1)/n [computed]. They go through Jacobi sums at a cross ratio λ that (C1)
  forces into Q₀ [argued: uniformity of the (C1) weight on λ is not proved].
- (2,3) classes and classes with both supports ≥ 3 decay faster [computed].

## 5. General κ

**Corollary 5 [proved mod Weil; computed by weights.py].**
- Assume p > (κ−1)κ^{κ−1} + κ−1, the pigeonhole bound for (C1) existence.
- Then PW < 1 for p ≥ T_abs(κ), with explicit bound T_abs ≤ (X+√(2κ))², where
  X = (2κ−2)((1+κ^{κ−1/2}/√κ!)²−1).

| κ | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|
| T_abs | 5.6·10³ | 5.3·10⁶ | 5.3·10⁹ | 4.1·10¹² | 1.25·10¹⁶ | 3.2·10¹⁹ |
| T_A | 54 | 768 | 1.25·10⁴ | 2.3·10⁵ | 4.9·10⁶ | 1.2·10⁸ |

- This is about T_A^{2+o(1)}, so nothing new is covered.
- The loss is the permanent weight W_tot ≈ (eκ)^κ. Even a uniform O(κ/p) bound on every class
  would give only about e^κκ^{κ+1/2}.

**Conjecture OSC(B) [open].**
- (N) The (C1) count satisfies N₁ ≥ p^{2κ−2}κ^{−(κ−1)²}/B.
- (L) |F̂| ≤ BκF̂(0)/p for ρ ∉ 𝓟 with m ≤ 5.
- (H) |F̂| ≤ B√(m/N₁)F̂(0) for all other ρ ≠ 0: square-root cancellation over the (C1) orbits.

Under OSC(B), PW_pair < 1 for p ≥ T_strong(B):

| κ | T_strong(1) | T_strong(4) | T_H(1) | 1.5κ^{(κ+1)/2} | T_A |
|---|---|---|---|---|---|
| 4 | 641 | 2633 | 81 | 48 | 768 |
| 5 | 3450 | 1.4·10⁴ | 336 | 188 | 1.25·10⁴ |
| 6 | 1.2·10⁴ | 4.7·10⁴ | 1335 | 794 | 2.3·10⁵ |
| 7 | 3.6·10⁴ | 1.4·10⁵ | 6308 | 3602 | 4.9·10⁶ |
| 8 | 9.1·10⁴ | 3.6·10⁵ | 3.0·10⁴ | 1.7·10⁴ | 1.2·10⁸ |
| 9 | 2.2·10⁵ | 8.0·10⁵ | 1.53·10⁵ | 8.9·10⁴ | 3.1·10⁹ |

- T_strong = κ^{(κ+1)/2+o(1)}.
- A weak form, with (L) for every class of min-support ≤ 2, gives T_weak(1) = 1.1·10³, 1.1·10⁴,
  9.5·10⁴, 1.0·10⁶, 1.0·10⁷ for κ = 4..8.
- Empirical constants [computed]:
  - B_L ≤ 1.85;
  - B_H is 2.7–6.1 at κ = 3 and 6–27 at κ = 4;
  - N₁/μ₁ is 0.15–0.92.
- Caveat: every tested prime has mean bucket size p/κ^{κ−1} ≳ 0.3. The conjectured regime has
  that ≪ 1 and is untested. κ = 5 near p ≈ 3·10³ is the first real test.

## 6. Claim gates (stay false)

- OSC is proved.
- The certificate is proved below T_A for any infinite family.
- Any threshold or table changes.
- "Low-support ≈ κ/p" holds for every one-sided class.
- This report is human-reviewed.

## 7. Next

- Test (N) and (H) at κ = 5 for p ≈ 3·10³ with an orbit-based enumerator.
- Or prove (H) for the (3,3) classes at κ = 4 via the λ-moduli expansion.
