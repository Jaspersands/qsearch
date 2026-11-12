# Verdict on the polynomial-pencil regularization lemma

**Verdict.** All three claims survive the cheapest attacks, and each has a complete proof (below). The composed lemma also holds: one random u, polynomially many bits deep, makes Res(f,A_u) and Disc(A_u) visibly nonzero and controls every mixed Res(W,A_u), all at once. The lemma is **conditional on the stated caps**, and in particular on joint caps for every half, which nothing here proves.

Required corrections:

- **(a) Claim 2's exact sign.** The leading coefficient is (−1)^{N(N−1)/2}·N^N·Disc(a), with N = m−e and Disc(a) = ∏_{i<j}(α_i−α_j)².
- **(b) Claim 3 needs no rounding constant.** The exact bound is ≤ d·2^{−(⌊t/d⌋+1)}. Integrality is not needed for the Haar statement, only for the grid transfer.
- **(c) Denominator clearing is explicit.** The mixed scaling is 2^{gS+mT}. The discriminant scaling is 2^{(2m−2)S}.
- **(d) Degree of W.** Use deg W = w ≤ g, not "= g".
- **(e) Cap on Res(W,f) is an assumption.** A derivative fallback is noted for when it fails.
- **(f) Grid depth B uses the assumed W caps.** The algorithm must know those caps as explicit numerical bounds.

No new statement here establishes a speedup, a hardness result, or ONE-HALF.

---

## 0. Cheapest attacks (all consistent; they are controls, not proofs)

**Claim 2, case e=0, g=1.** Take f = x³+px+q, so A_u = f−u².
- Disc(A_u) = −4p³−27(q−u²)² = −27u⁴ + 54qu² − 27q² − 4p³.
- The degree is 4 = 4g. The leading coefficient −27 = (−1)^{3}·3³ matches the corrected formula.

**Claim 2, case e=1, g=1, so N=1.** Take a = x−α, b = β, c = x²+c₁x+c₀.
- A_u = x² + (c₁−u²)x + (c₀−2uβ+αu²).
- Disc(A_u) = u⁴ − (2c₁+4α)u² + 8βu + c₁² − 4c₀.
- The leading coefficient is 1 = Disc(a), as predicted.

**Claim 2, case e=1, g=2, so N=3.** Take a = x, b = 0, c = x⁴, so A_u = x(x³−u²).
- Disc(A_u) = Disc(x)·Disc(x³−u²)·Res(x, x³−u²)² = (−27u⁴)(u⁴) = −27u⁸.
- The degree is 8 = 4g with leading coefficient −27, as predicted.

**Claim 3, falling factorials.** Take P = ∏_{i<d}(u−i).
- Here P is monic with content 0, yet v₂P(u) ≥ v₂(d!) for every u.
- The bound d·2^{−t/d} is ≥ 1 whenever t ≤ d·log₂ d, and v₂(d!) < d ≤ d·log₂ d.
- So no violation occurs. This was the natural place to break a valuation-tail claim.

**Claim 1, extremal cases.** If a(β) = b(β) = c(β) = 0, then f(β) = f'(β) = 0, which is impossible for squarefree f. So A_u(β) is never identically zero in u.

---

## 1. Claim 1: proved, with explicit scaling

**Proof.** Let β be any root of W in a splitting field.
1. Since f = b² + ac, we have f(β) = b(β)² + a(β)c(β).
2. Put μ_β = min(v c(β), 1+v b(β), v a(β)).
3. Then v f(β) ≥ min(2v b(β), v a(β)+v c(β)) ≥ min(2μ_β−2, 2μ_β) = 2μ_β − 2.
4. Hence μ_β ≤ 1 + v f(β)/2.
5. μ_β is exactly the Gauss valuation of c(β) − 2u·b(β) − u²·a(β) ∈ K[u].

Now assemble the resultant.
- W is monic of degree w ≤ g, so Res_x(W,A_u) = ±∏_β A_u(β), with multiplicity. W need not be squarefree.
- The Gauss norm on K[u] is multiplicative over any non-archimedean field (Gauss's lemma).
- Therefore content_u(R_W) = Σ_β μ_β ≤ w + Σ_β v f(β)/2 = w + v Res(W,f)/2 ≤ g + v Res(W,f)/2.
- No signed cancellation is used; this is a per-root Gauss bound.
- deg_u R_W ≤ 2w ≤ 2g, with u^{2w} coefficient ±Res(W,a).
- The bound requires Res(W,f) ≠ 0, which is the assumed finite branch cap.

**Scaling.** Assume the A_u x-coefficients, viewed as polynomials in u, have u-coefficients of valuation ≥ −S. Assume W's coefficients have valuation ≥ −T in O_K.
- In the Sylvester matrix, the m rows of W times 2^T are integral, and the w rows of A_u times 2^S are integral.
- So P_W := 2^{gS+mT}·R_W ∈ O_K[u].
- Its content is γ_W ≤ g + ρ/2 + gS + mT, where ρ is the cap on v Res(W,f).
- This is the "more if W is nonintegral" charge: mT, which is linear in the pole depth.

**Fallback if some half's support hits a Weierstrass point.** In that case Res(W,f) = 0 and the claimed bound is vacuous. A derivative bound still applies at every β:
- From f' = 2bb' + a'c + ac', we get v f'(β) ≥ μ_β + min(v b'(β), v a'(β), v c'(β)).
- So μ_β ≤ v f'(β) + L_β, where L_β is the pole/derivative loss at β.
- This would replace ρ/2 by roughly v Res(W,f') + Σ L_β.
- This is offered as a conditional repair, not checked further.

---

## 2. Claim 2: proved over characteristic zero

**Setup.** Work in the Puiseux field 𝕂 = ⋃_k \bar{ℚ}₂((s^{1/k})), with s = 1/u. 𝕂 is algebraically closed because ℚ̄₂ has characteristic 0. Disc_x(A_u) ∈ ℚ₂[u] embeds in 𝕂. Its u-degree and leading coefficient equal −ord_s and the leading s-coefficient of its expansion.

**Roots via the Newton polygon.** Write −s²A_u = a(x) + 2s·b(x) − s²·c(x), a polynomial in x over \bar{ℚ}₂[s] with leading coefficient −s² at x^m.
- Plot the points (j, ord_s coeff_j).
  - For j ≤ e, ord is ≥ 0, with ord = 0 at j = e because a is monic.
  - For e < j ≤ m, ord is ≥ 2, with ord = 2 at j = m.
- The segment from (e,0) to (m,2) has slope 2/N. For e < j < m its height 2(j−e)/N is < 2, so no point lies below it.
- **Small roots.** e roots have ord ≥ 0. Reducing mod s gives a(x), which is squarefree. Hensel's lemma then gives e distinct roots r_i ≡ α_i (mod s^{>0}).
- **Large roots.** N roots have ord = −2/N, i.e. ρ_k = s^{−2/N}·y_k(1+o(1)). The residual equation is ρ^e − s²ρ^m = ρ^e(1−y^N), so y_k^N = 1. The y_k are distinct because the characteristic is 0.
- The b-term has ord ≥ 1 and lies off the polygon, so it never matters. Poles or non-integrality in a, b, c are irrelevant because the argument is over ℚ₂.

**Leading terms.** Since A_u is monic, Disc = ∏_{i<j}(root differences)². Group the factors:
- **Small–small:** tends to Disc(a), which is nonzero because a is squarefree.
- **Large–large:** u^{2(N−1)}·Disc(x^N−1) = (−1)^{N(N−1)/2}·N^N·u^{2(N−1)}, using N odd.
- **Cross terms:** ∏_{i,k}(ρ_k−α_i)² gives leading part (∏_k ρ_k)^{2e} = (u²·∏ω_k)^{2e} = u^{4e}. Here ∏_k ω_k = 1 because N is odd.

**Result.**
- The exponent is 2(N−1) + 4e = 2m + 2e − 2 = 2n − 2 = 4g.
- The leading coefficient is (−1)^{N(N−1)/2}·N^N·Disc(a), exactly.
- The edge case e = 0 recovers Disc(f−t) = ±n^n·t^{n−1} with t = u².

**Content.** v(N^N) = 0 since N is odd, so content(Disc A_u) ≤ v Disc(a).

**Integral version.** P_D := Disc_x(2^S A_u) = 2^{(2m−2)S}·Disc_x(A_u) ∈ ℤ₂[u].
- Its degree is 4g.
- Its content is γ_D ≤ (2m−2)S + v Disc(a).
- An upper cap on v Disc(a) is needed. It is computable from the given a.

---

## 3. Claim 3: proved, no rounding constant

**Proof.** Let P ∈ K[u] be nonzero, of degree d, over a finite extension K/ℚ₂, with content γ = v(Gauss norm). Factor P = λ∏(u−r_i) over \bar{ℚ}₂.
1. The Gauss norm satisfies γ = v λ + Σ_i min(0, v r_i).
2. For u ∈ ℤ₂, v(u−r_i) = v r_i whenever v r_i < 0.
3. Hence v P(u) − γ = Σ_{i: v r_i ≥ 0} v(u−r_i). Every term is ≥ 0, and there are ≤ d terms.
4. If the sum exceeds t, some root r_i has v(u−r_i) > t/d.
5. Fix such an r_i. If u, u′ ∈ ℤ₂ both satisfy this, then v(u−u′) > t/d. Since v(u−u′) is an integer, v(u−u′) ≥ ⌊t/d⌋+1. This holds also when r_i ∉ ℚ₂ or v r_i is fractional.
6. So the bad set for each root lies in one ball of Haar measure 2^{−⌊t/d⌋−1}.
7. A union bound over ≤ d roots gives:

   **Pr(v P(u) > γ + t) ≤ d·2^{−⌊t/d⌋−1} < d·2^{−t/d}.**

Note that d·2^{−t/d} is increasing in d, so a degree upper bound suffices.

**Exact grid transfer.** If P ∈ O_K[u] and u ≡ u′ (mod 2^{K+1}), then P(u) ≡ P(u′) (mod 2^{K+1}·O_K). So the event {v P(u) ≤ K} depends only on u mod 2^{K+1}.
- A uniform integer in [0, 2^B) with B ≥ K_j + 1 for all j reproduces the joint Haar law of all these events exactly.
- Integral scaling is required for this step, not for the tail bound itself.

**Why Markov fails.** E[v P(u) − γ] ≤ d, since E[v(u−r)] ≤ 1. Markov then gives d/t, and a union over 2^{2g} halves would force t ~ g·2^{2g}, an exponential valuation depth. The exponential tail in Claim 3 is essential.

---

## 4. Composition: thresholds and bit depth (conditional)

Fix a target λ, for example λ = cg. Use three integral polynomials in u.

| Polynomial | Degree in u | Content cap C_j |
|---|---|---|
| P_br = Res_x(f, 2^S A_u) ∈ ℤ₂[u] | ≤ 2n | C_br = v disc f + 2nS |
| P_D = Disc_x(2^S A_u) | 4g | C_D = (2m−2)S + v Disc(a) |
| P_W, one per half Q | ≤ 2g | C_W = g + ρ/2 + gS + mT |

- **Source of C_br.** I rechecked the note's proof sketch. At each root θ of f, μ_θ ≤ v f′(θ) + S from the derivative identity. Summing gives v disc f + nS, and the scaling adds nS. The note's bound assumes S also bounds the derivative coefficients.
- **Joint caps on W.** ρ and T are the joint caps over all ≤ 2^{2g} halves. There are at most #J[2] = 2^{2g} halves, whether rational or geometric.

**Tail allowances.**
- t_br = 2n(λ + 2 + log₂ 2n)
- t_D = 4g(λ + 2 + log₂ 4g)
- t_W = 2g(λ + 2 + 2g + log₂ 2g)

**Thresholds and depth.** Set K_j = ⌈C_j + t_j⌉ and B = max_j K_j + 1.

**Probability bound.** By Claim 3, applied to each polynomial separately (no product polynomial):
- P(bad_br) ≤ 2^{−λ−2} and P(bad_D) ≤ 2^{−λ−2}.
- P(some half is bad) ≤ 2^{2g}·2g·2^{−t_W/2g} ≤ 2^{−λ−2}.
- So the total failure probability is < 2^{−λ}, and the bit depth is B = O(g² + gλ + nS + mT + caps).

**Conditioning on acceptance.** The algorithm resamples until the visible checks pass. Per draw, Pr(mixed bad | visible pass) ≤ 2^{−λ}/(1−2^{−λ}). The expected number of draws is ≤ 1 + O(2^{−λ}). With λ draws, the probability that none passes is negligible.

---

## 5. What the algorithm can see, and branch circularity

**Visible checks.**
- v P_br(u) ≤ K_br and v P_D(u) ≤ K_D are decided by Smith/Hermite elimination of the Sylvester matrices over ℤ/2^{K+1}.
- Passing certifies that A_u is squarefree and coprime to f, with explicit conditioning.

**Invisible check.** v P_W(u) ≤ K_W is never evaluated, because W is unknown. It is controlled only in probability. Actual acceptance must come from the later Stoll augmented-matrix certificate, and a rejection there must trigger resampling.

**Circularity: none in what is stated.**
- A_u, Res, and Disc lie in ℚ₂[x] and use no square-root branch.
- Res_x(W, A_u) is branch-blind: it controls x-coincidence with both P and ι(P).
- The set of halves depends only on the class [a,b], which [A_u,b_u] preserves, so it is fixed before u is drawn.
- The caps are assumed jointly for all halves in advance.

**Circularity would appear if:**
- (i) the W-caps were proved via a representation built from u or [A_u,b_u]; or
- (ii) the relevant halves were defined after u, for example "halves avoiding A_u"; or
- (iii) the Stoll certificate needs a branch-dependent quantity that this x-resultant does not control.

---

## 6. Cost charges

- **Randomness:** B bits per draw.
- **Arithmetic:** determinants of size ≤ 4g+2 over ℤ/2^{K+1}, costing poly(g, B) bit operations.
- **Input precision:** a and b must be known well enough that the entries of 2^S A_u are correct mod 2^{K_max+1}. That means precision about K_max + 1 plus the monic-division loss O(mS₀), and it must be re-derived; the note's "Kbr+S+1" covers the resultant only.
- **Output:** u (B bits) and A_u, b_u at that precision.
- **Unchargeable here:** the cost of materializing [a,b], the caps on W, and acceptance by the Stoll certificate.
- No quantum resource, speedup, or hardness claim arises.

---

## 7. Status of each gate

**Proved:**
- Claim 1, including the scaling 2^{gS+mT}.
- Claim 2, with the exact constant (−1)^{N(N−1)/2}·N^N·Disc(a).
- Claim 3, plus exact grid transfer for integral polynomials over O_K.
- The union-bound arithmetic of §4.

**Conditional (assumed, not proved here):**
- Polynomial S, S₀, and the caps on v Disc(a) and v disc f.
- Joint polynomial caps ρ and T for all halves, which the algorithm must know as explicit numerical bounds in order to set B.
- Squarefree a.
- The note's branch content bound C_br, which I rechecked only in sketch.

**Open:**
- Materializing [a,b] from h + 2σ(z).
- Precision propagation through c = (f−b²)/a for P_D.
- A Haar-to-σ stability radius.
- Stoll certificate acceptance.
- ONE-HALF.

**Falsifiers to look for:**
- A native f with a rational class [a,b] where some half's reduced W contains a Weierstrass point, has super-polynomial pole depth T, or has super-polynomial v Res(W,f). Any of these breaks the joint-cap assumption, not the lemma.
- A downstream certificate whose conditioning needs a branch-signed or Cantor-composed quantity not bounded by Res_x(W, A_u).